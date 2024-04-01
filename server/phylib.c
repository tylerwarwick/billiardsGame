#include "phylib.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Constructors functions
phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos) {
  phylib_object *newObj = NULL;

  // If malloc fails, return NULL
  if ((newObj = malloc(sizeof(phylib_object))) == NULL)
    return NULL;

  // Set our object type to still ball
  newObj->type = PHYLIB_STILL_BALL;

  // Intialize values for our still ball
  phylib_still_ball *ball = (phylib_still_ball *)&(newObj->obj);

  // Store our parameters as the ball's properties
  ball->number = number;
  ball->pos = *pos;

  return newObj;
}

phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos,
                                       phylib_coord *vel, phylib_coord *acc) {
  phylib_object *newObj = NULL;

  // If malloc fails, return NULL
  if ((newObj = malloc(sizeof(phylib_object))) == NULL)
    return NULL;

  // Set our object type to rolling ball
  newObj->type = PHYLIB_ROLLING_BALL;

  // Intialize values for our rolling ball
  phylib_rolling_ball *ball = (phylib_rolling_ball *)&(newObj->obj);

  // Store our parameters as the rollings ball's properties
  ball->number = number;
  ball->pos = *pos;
  ball->vel = *vel;
  ball->acc = *acc;

  return newObj;
}

phylib_object *phylib_new_hole(phylib_coord *pos) {
  phylib_object *newObj = NULL;

  // If malloc fails, return NULL
  if ((newObj = malloc(sizeof(phylib_object))) == NULL)
    return NULL;

  // Set our object type to hole
  newObj->type = PHYLIB_HOLE;

  // Intialize values for our hole
  phylib_hole *hole = (phylib_hole *)&(newObj->obj);

  // Store our parameters as the hole's properties
  hole->pos = *pos;

  return newObj;
}

phylib_object *phylib_new_hcushion(double y) {
  phylib_object *newObj = NULL;

  // If malloc fails, return NULL
  if ((newObj = malloc(sizeof(phylib_object))) == NULL)
    return NULL;

  // Set our object type to hcushion
  newObj->type = PHYLIB_HCUSHION;

  // Intialize values for our hcushion
  phylib_hcushion *cushion = (phylib_hcushion *)&(newObj->obj);

  // Store our parameters as the cushion's properties
  cushion->y = y;

  return newObj;
}

phylib_object *phylib_new_vcushion(double x) {
  phylib_object *newObj = NULL;

  // If malloc fails, return NULL
  if ((newObj = malloc(sizeof(phylib_object))) == NULL)
    return NULL;

  // Set our object type to hcushion
  newObj->type = PHYLIB_VCUSHION;

  // Intialize values for our vcushion
  phylib_vcushion *cushion = (phylib_vcushion *)&(newObj->obj);

  // Store our parameters as the cushion's properties
  cushion->x = x;

  return newObj;
}

phylib_table *phylib_new_table(void) {
  phylib_table *table = NULL;

  // If malloc fails, return NULL
  if ((table = malloc(sizeof(phylib_table))) == NULL)
    return NULL;

  // Initialize every index to NULL initially
  // Will make sure we get no undefined references in valgrind
  for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
    table->object[i] = NULL;
  }

  // Now initialize necessary values
  // Initial time is 0
  table->time = 0.0;

  // 4 cushions to form border of table
  table->object[0] = phylib_new_hcushion(0.0);
  table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
  table->object[2] = phylib_new_vcushion(0.0);
  table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

  // 6 holes starting from top left and working around table clockwise
  // Holes need to be off wall by one ball diameter (hole has diameter twice
  // that of pool ball) (we are not recessing holes in wall) Top left
  table->object[4] = phylib_new_hole(&(phylib_coord){0, 0});

  // Left middle
  table->object[5] =
      phylib_new_hole(&(phylib_coord){0, PHYLIB_TABLE_LENGTH / 2});

  // Bottom Left
  table->object[6] = phylib_new_hole(&(phylib_coord){0, PHYLIB_TABLE_LENGTH});

  // Top right
  table->object[7] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, 0});

  // Middle right
  table->object[8] = phylib_new_hole(
      &(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH / 2});

  // Bottom right
  table->object[9] =
      phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH});

  return table;
}

/*
There are a couple philosophies when creating/storing objects in the table array
1. We could store them starting from the front, meaning that whenever we need to
iterate/query, we can terminate our iteration when we reach a NULL index (we've
iterated over every object in the array at this point). This cuts down time on
the number of iterations. (However I concede that when calculating time
complexity any constants get discarded (so O(13/16 n) is ultimately just O(n))).
This would also mean anytime we need to remove/free an index, we would need to
resort our array to have all the NULL indexes reshuffled to the back of the
array.

2. We store them wherever a NULL index can be located first (for the most part
this will be the same as previous case). The difference is then that we cannot
terminate our iterative processes when we encounter a NULL index. This means
when we need to completely iterate over the whole array for every process.
However we would not need to sort our array ever.

So my question is which is better? Is there a method the project is built
around?

I will go ahead and implement the second method tentatively, atleast then I can
achieve the functionality and worry about optimization later. Also as the number
of objects approached 26, there is little benefit to the first method as we
incur little to no iteration savings and we have to constantly resort a near
full array for no benefit.
*/

// Utitlity functions
void phylib_copy_object(phylib_object **dest, phylib_object **src) {
  // If source is null, point dest to NULL and exit
  if (*src == NULL) {
    *dest = NULL;
    return;
  }

  // Allocate memory for new object
  phylib_object *srcCopy = malloc(sizeof(phylib_object));

  // If malloc fails, return
  if (srcCopy == NULL)
    return;

  // Copy contents at source to new memory we just created
  memcpy(srcCopy, *src, sizeof(**src));

  // Point dest to location of newly created memory that has been loaded with
  // src content
  *dest = srcCopy;
}

phylib_table *phylib_copy_table(phylib_table *table) {

  phylib_table *newTable = malloc(sizeof(phylib_table));

  // If malloc fails, return NULL
  if (newTable == NULL)
    return NULL;

  // Copy time to new table
  newTable->time = table->time;

  // Initialize all of new table's pointers to NULL initially
  for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
    newTable->object[i] = NULL;
  }

  for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
    // If index value is null, we've copied all values (DEPRECATED)
    // if (table->object[i] == NULL) break;

    // Can't simply point to same address or else delete gets sticky
    // Need to create new copy of memory
    phylib_copy_object(&newTable->object[i], &table->object[i]);
  }

  return newTable;
}

void phylib_add_object(phylib_table *table, phylib_object *object) {
  for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
    // If we find empty index, populate it
    if (table->object[i] == NULL) {
      table->object[i] = object;

      // We've done what we set out to do, exit loop and therefore function
      break;
    }
  }
}

void phylib_free_table(phylib_table *table) {
  // Check we are being passed a table
  if (table == NULL)
    return;

  // Need to quickly iterate over object array, freeing anything needed to be
  // freed
  for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
    // If we find empty index, we've freed everything (DEPRECATED)
    // New system means we simply skip a NULL index
    if (table->object[i] == NULL)
      continue;
    ;

    // Free memory in table
    free(table->object[i]);

    // Set pointer at the index back to NULL
    table->object[i] = NULL;
  }

  // Go ahead and free the table struct itself
  free(table);
}

phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2) {
  // Return coord with components as differences between two parameters
  return (phylib_coord){c1.x - c2.x, c1.y - c2.y};
}

double phylib_length(phylib_coord c) {
  // Get magnitude of vector
  return sqrt((c.x * c.x) + (c.y * c.y));
}

double phylib_dot_product(phylib_coord a, phylib_coord b) {
  return (a.x * b.x) + (a.y * b.y);
}

// Helper function to get magnitude difference between 2 vectors
double magnitudeDifference(phylib_coord c1, phylib_coord c2) {
  // Get vector of distances between 2 bodies
  phylib_coord distanceVector = phylib_sub(c1, c2);

  // Return magnitude of that vector of differences
  return fabs(phylib_length(distanceVector));
}

double phylib_distance(phylib_object *obj1, phylib_object *obj2) {
  // If object 1 isn't a rolling ball, stop here and return a negative value to
  // indicate invalid parameters
  if (obj1->type != PHYLIB_ROLLING_BALL)
    return -1.0;

  // Declare object 1 coords here as we will use in every case possible
  phylib_coord obj1Coords = obj1->obj.rolling_ball.pos;

  // We could type check 2nd object to look for one of the 4 possible types
  // Instead I will clause guard and our default action taken will be returning
  // -1.0 if no conditions are met Case 1: 2nd object is another ball
  if (obj2->type == PHYLIB_STILL_BALL || obj2->type == PHYLIB_ROLLING_BALL) {

    // Get distance between bodies
    double distance =
        (obj2->type == PHYLIB_STILL_BALL)
            ? magnitudeDifference(obj1Coords, obj2->obj.still_ball.pos)
            : magnitudeDifference(obj1Coords, obj2->obj.rolling_ball.pos);

    // Return distance apart remembering to subtract the radii of both balls
    return distance - PHYLIB_BALL_DIAMETER;
  }

  // Case 2: 2nd object is hole
  if (obj2->type == PHYLIB_HOLE) {
    // Return distance between remembering to subtract radius of hole
    return magnitudeDifference(obj1Coords, obj2->obj.hole.pos) -
           PHYLIB_HOLE_RADIUS;
  }

  // Case 3: 2nd object is a cushion
  if (obj2->type == PHYLIB_HCUSHION || obj2->type == PHYLIB_VCUSHION) {
    // Get distance between bodies
    double distance = (obj2->type == PHYLIB_HCUSHION)
                          ? obj1Coords.y - obj2->obj.hcushion.y
                          : obj1Coords.x - obj2->obj.vcushion.x;

    // Return distance apart remembering to subtract the radius of the ball
    return fabs(distance) - PHYLIB_BALL_RADIUS;
  }

  // As mentioned, if none of those cases were met, we have not yet returned and
  // therefore object 2 is not a valid type We will return negative value
  // indicating faulty parameter passed
  return -1.0;
}

// Helper function calculating displacement
double displacement(double vel, double acc, double time) {
  return (vel * time) + (0.5 * acc * time * time);
}

// Dynamics functions
void phylib_roll(phylib_object *new, phylib_object *old, double time) {
  // If both are not rolling balls, nothing can be done in this context
  if (!(new->type == PHYLIB_ROLLING_BALL && old->type == PHYLIB_ROLLING_BALL))
    return;

  // Typecast to rolling balls to make easier to work with
  phylib_rolling_ball *newBall = (phylib_rolling_ball *)&new->obj;
  phylib_rolling_ball *oldBall = (phylib_rolling_ball *)&old->obj;
  
  // Calculate new positions
  newBall->pos.x =
      oldBall->pos.x + displacement(oldBall->vel.x, oldBall->acc.x, time);
  newBall->pos.y =
      oldBall->pos.y + displacement(oldBall->vel.y, oldBall->acc.y, time);

  // Calculate new velocity
  newBall->vel.x = oldBall->vel.x + (oldBall->acc.x * time);
  newBall->vel.y = oldBall->vel.y + (oldBall->acc.y * time);

  // Check that velocities have not changed direction
  // Trick here is that if the signs match, their product will be positive
  // If we get a negative product, we need to set our vel and acc to 0
  if ((newBall->vel.x * oldBall->vel.x) < 0.0) {
    newBall->vel.x = 0.0;
    newBall->acc.x = 0.0;
  }

  if ((newBall->vel.y * oldBall->vel.y) < 0.0) {
    newBall->vel.y = 0.0;
    newBall->acc.y = 0.0;
  }
}

unsigned char phylib_stopped(phylib_object *object) {
  // Again we will guard clause
  // If magnitude of velocity is less than vel epsilon, convert rolling ball to
  // still ball
  if (phylib_length(object->obj.rolling_ball.vel) < PHYLIB_VEL_EPSILON) {
    // Keep a copy of our position coords before typecasting
    phylib_coord temp = object->obj.rolling_ball.pos;

    // Set object type
    object->type = PHYLIB_STILL_BALL;

    // Typecast actual object
    phylib_still_ball *stillBall = (phylib_still_ball *)&(object->obj);

    // Refresh pos values (can't assume they transfer)
    stillBall->pos = temp;

    // Indicate a conversion occured
    return 1;
  }

  // 0 will be our default return value (no conversion occurs)
  return 0;
}

// Bounce is growing in size so I'm gonna pull the rolling ball calculations out
// into their own function Could do for all but rolling ball is most
// complicated, so I'll just do it for the one case We can make our parameters
// of type rolling_ball to rid ourselves of countless dereferencing
void rollingBallCollision(phylib_rolling_ball *a, phylib_rolling_ball *b) {
  // Finding relative position of a with respect to b
  phylib_coord r_ab = phylib_sub(a->pos, b->pos);

  // Find relative velocity of a with respect to b (he has it backwards in
  // instructions)
  phylib_coord v_rel = phylib_sub(a->vel, b->vel);

  // Find normal vector by dividing relative distance vector by it's magntiude
  phylib_coord n = (phylib_coord){r_ab.x / phylib_length(r_ab),
                                  r_ab.y / phylib_length(r_ab)};

  // Find relative velocity of a with respect to b along the line of impact by
  // taking dot product of relative velocity and normal vectors
  double v_rel_n = phylib_dot_product(v_rel, n);

  // Finally update the velocities via the conservation of momentum (negative
  // for a and additive for b) Ball a
  a->vel =
      (phylib_coord){a->vel.x - (v_rel_n * n.x), a->vel.y - (v_rel_n * n.y)};

  // Ball b
  b->vel =
      (phylib_coord){b->vel.x + (v_rel_n * n.x), b->vel.y + (v_rel_n * n.y)};

  // Addressing acceleration
  // If speed is greater than constant epsilon value we set, we need to update
  // accelerations Ball a
  double speedA = phylib_length(a->vel);
  if (speedA >= PHYLIB_VEL_EPSILON)
    a->acc = (phylib_coord){((-(a->vel.x) / speedA) * PHYLIB_DRAG),
                            ((-(a->vel.y) / speedA) * PHYLIB_DRAG)};

  // Ball b
  double speedB = phylib_length(b->vel);
  if (speedB >= PHYLIB_VEL_EPSILON)
    b->acc = (phylib_coord){((-(b->vel.x) / speedB) * PHYLIB_DRAG),
                            ((-(b->vel.y) / speedB) * PHYLIB_DRAG)};
}

void phylib_bounce(phylib_object **a, phylib_object **b) {
  // Assuming object a is rolling ball
  // We'll just typecast quickly to make it easier to work with
  phylib_rolling_ball *ball = (phylib_rolling_ball *)&((*a)->obj);

  switch ((*b)->type) {
  case PHYLIB_HCUSHION:
    // We've hit a upper/lower bound, reverse the Y vel and acc
    ball->vel.y = -(ball->vel.y);
    ball->acc.y = -(ball->acc.y);
    break;

  case PHYLIB_VCUSHION:
    // We've hit a left/right bound, reverse the x vel and acc
    ball->vel.x = -(ball->vel.x);
    ball->acc.x = -(ball->acc.x);
    break;

  case PHYLIB_HOLE:
    // Instructions say free hole (likely a mistake)
    // I will free ball and if for some reason its meant to be hole, I'll come
    // back and fix it

    // Need to dereference once so that I am freeing the address of the object
    // that is being pointed to twice
    free(*a);

    // Need to set pointer to NULL (that's why we have double pointer)
    *a = NULL;

    break;

  case PHYLIB_STILL_BALL: {
    /*
    I think we are to assume starting velocity and acceleration are 0. As far as
    calculating relative velocities, this makes sense to me.
    */
    // When we went from rolling to still we didn't assume position vector
    // transferred We will work under that same assumption and set it explicitly
    // Make a copy of coords quickly
    phylib_coord coordCpy = (*b)->obj.still_ball.pos;

    // Update untyped object type specifier
    (*b)->type = PHYLIB_ROLLING_BALL;

    // Refresh rolling ball's position in case it was lost along the way
    (*b)->obj.rolling_ball.pos = coordCpy;

    // It is being upgraded to a rolling ball but it's vel and acc are 0 before
    // being hit Set velocity
    (*b)->obj.rolling_ball.vel = (phylib_coord){(double)0.0, (double)0.0};

    // Set acceleration
    (*b)->obj.rolling_ball.acc = (phylib_coord){(double)0.0, (double)0.0};

    // No break statement here so that we may procede
    // with new scenario as rolling ball
  }
  case PHYLIB_ROLLING_BALL:
    // We'll pass just the actual rolling ball objects by reference to our
    // helper function As far as calculations go, the object wrapper is not
    // necessary
    rollingBallCollision((phylib_rolling_ball *)&((*a)->obj),
                         (phylib_rolling_ball *)&((*b)->obj));
    break;

  default:
    break;
  }
}

unsigned char phylib_rolling(phylib_table *t) {

  // Need to initialize a counter
  unsigned char rollingBalls = 0;

  for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
    // If we find empty index, we've checked out all objects on the table
    // (DEPRECATED) If we find an empty index, skip it
    if (t->object[i] == NULL)
      continue;
    ;

    // Increment rolling balls counter if we find one
    if (t->object[i]->type == PHYLIB_ROLLING_BALL)
      rollingBalls++;
  }

  return rollingBalls;
}

// Helper function to determine if these balls are headed towards or away from
// one another If I use kinematics and the distance between them increases, they
// are headed away Otherwise they are headed towards one another
double incidentPaths(phylib_object *obj1, phylib_object *obj2) {
  // Get original distance
  double originalDistance = phylib_distance(obj1, obj2);

  // Make copies of both objects and simulate them both a very small time in the
  // future I don't know what type of object it is; so I'll make a helper
  // function to make me the correct copy Get a copy of each object
  phylib_object *futureObj1 = NULL;
  phylib_object *futureObj2 = NULL;
  phylib_copy_object(&futureObj1, &obj1);
  phylib_copy_object(&futureObj2, &obj2);

  // Ball 1
  // Only need to simulate displacement for one sim rate if obj is rolling ball
  if (futureObj1->type == PHYLIB_ROLLING_BALL) {
    // Make a pointer to make life easier
    phylib_rolling_ball *ball = (phylib_rolling_ball *)&futureObj1->obj;
    ball->pos.x =
        ball->pos.x + displacement(ball->vel.x, ball->acc.x, PHYLIB_SIM_RATE);
    ball->pos.y =
        ball->pos.y + displacement(ball->vel.y, ball->acc.y, PHYLIB_SIM_RATE);
  }

  // Ball 2
  // Only need to simulate displacement for one sim rate if obj is rolling ball
  if (futureObj2->type == PHYLIB_ROLLING_BALL) {
    // Make a pointer to make life easier
    phylib_rolling_ball *ball = (phylib_rolling_ball *)&futureObj2->obj;
    ball->pos.x =
        ball->pos.x + displacement(ball->vel.x, ball->acc.x, PHYLIB_SIM_RATE);
    ball->pos.y =
        ball->pos.y + displacement(ball->vel.y, ball->acc.y, PHYLIB_SIM_RATE);
  }

  // If future objects are closer after a sim than older objects, they have
  // incident paths
  if (phylib_distance(futureObj1, futureObj2) < originalDistance) {
    // Need to free here as well incase this control path is followed
    free(futureObj1);
    free(futureObj2);

    // Send flag to indicate these two objects are in fact on incident paths
    return 1;
  }

  // Make sure to free up the clones we created for the comparison
  free(futureObj1);
  free(futureObj2);

  // Otherwise they are not incident, we can return 0 to indicate no
  return 0;
}

// Helper function to determine if objects will collide
double willCollide(phylib_object *obj1, phylib_object *obj2) {
  // If neither is rolling ball, we can't have a collision
  if (obj1->type != PHYLIB_ROLLING_BALL && obj2->type != PHYLIB_ROLLING_BALL)
    return 0;

  // Run comparisons for the case in which obj1 is rolling
  if (obj1->type == PHYLIB_ROLLING_BALL) {
    if (phylib_distance(obj1, obj2) <= 0.0 && incidentPaths(obj1, obj2))
      return 1;
    return 0;
  }

  // By default this will excecute if only obj2 is rolling ball
  if (phylib_distance(obj2, obj1) <= 0.0 && incidentPaths(obj2, obj1))
    return 1;
  return 0;
}

double impendingCollision(phylib_table *table) {
  for (int i = 0; i < PHYLIB_MAX_OBJECTS - 1; i++) {
    // If NULL skip it
    if (table->object[i] == NULL)
      continue;

    for (int j = i + 1; j < PHYLIB_MAX_OBJECTS; j++) {

      // If NULL skip it
      if (table->object[j] == NULL)
        continue;

      // If two objects are this close, we need to check if they are headed
      // toward or away from one another via helper func Need to compare both
      // ways
      if (willCollide(table->object[i], table->object[j])) {
        // If we find a pair of objects that are indeed going to collide
        // We need to call the bounce function with them
        // Need to call both ways as well
        // phylib_print_table(table);

        if (table->object[i]->type == PHYLIB_ROLLING_BALL)
          phylib_bounce(&table->object[i], &table->object[j]);
        else
          phylib_bounce(&table->object[j], &table->object[i]);

        // Return a 1 to indicate to sim function to return new simulated table
        return 1;
      }
    }
  }

  // If we couldn't find a collision, indicate as such
  return 0;
}

//**He says start at sim_rate but I can only assume he means start at internal
// time property of table
/*
Another cause for concern is that when a collision occurs, we call the bounce
function. This updates the involved objects' velocities and accelerations, but
will they not still be close enough to trigger the collision threshold the next
time we simulate? Must we simulate one round each time before checking for our
exit clauses??

UPDATE: I'll just create a helper function to determine if they are going to
collide or if they are headed away from one another
*/
phylib_table *phylib_segment(phylib_table *table) {
  // If we have no rolling balls, we have nothing to simulate
  if (phylib_rolling(table) == 0)
    return NULL;

  // Otherwise we need to simulate all collisions, one PHYLIB_SIM_RATE interval
  // at a time Unsure whether we'll be using old table for anything so I'll copy
  // it over to a new one and update it (leaving original untouched)
  phylib_table *newTable = phylib_copy_table(table);

  // If a ball has stopped, we are done
  // We'll use a flag do signal this inside the internal loop below
  double stoppedBall = 0;

  // We'll set an indefinite loop and just have many breakout clauses internally
  while (1) {
    // At the top of every cycle we need to check no exit clauses are met

    // If the time limit is reached, we are done simulating
    if (newTable->time >= PHYLIB_MAX_TIME)
      break;

    // If we have no rolling balls we are done
    if (phylib_rolling(newTable) == 0)
      break;

    // If the flag indicates a ball has come to a halt, we are also done
    // simulating
    if (stoppedBall)
      break;

    /*
    The hardest part is checking if any item in the object array are hitting one
    another.

    ** We'll have to check every distinct combination before returning, in case
    multiple collisions are occuring at one time. (REDACTED) **

    We can return the table as soon as we spot a impending collision, because
    even though we may have collisions going on concurrently; the next round of
    simulation with the new table will address it.

    This will likely be expensive as we have many embedded loops but this is a
    physics engine (written in c for a reason). I say that to convey that it is
    just the nature of the beast when it comes to simulating physics.

    Cutting down to brass tax, we will do it with a nested for loop. The inner
    loop will begin at the outter loops iterator (this will remove redundancy
    (bringing it to O(nlogn))). It will call the bounce function (and exit the
    loop) for any pair that meets the threshold for a collision to take place.
    I'll write this up in it's own helper function.
    */

    // Use our helper function to accomplish all of the aforementioned
    if (impendingCollision(newTable))
      break;

    // If none of our breakout conditions are met, simulate one cycle for every
    // ball Let ball roll for one sim_rate length
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
      // If NULL skip
      if (newTable->object[i] == NULL)
        continue;

      // Only simulate rolling if they are indeed rolling balls
      if (newTable->object[i]->type == PHYLIB_ROLLING_BALL) {
        // Need to make a new ball to copy info to
        phylib_object *simulatedBall;

        // Copy all the data first
        phylib_copy_object(&simulatedBall, &newTable->object[i]);

        // Then apply simulated roll changes
        phylib_roll(simulatedBall, newTable->object[i], PHYLIB_SIM_RATE);

        // Quickly check if it's stopped rolling
        // Stopped function will do the necesarry type conversions
        // We'll update our flag from loop above to let it know if we've had a
        // ball come to a stop
        stoppedBall = (phylib_stopped(simulatedBall) == 1) ? 1 : stoppedBall;

        free(newTable->object[i]);
        newTable->object[i] = simulatedBall;
      }
    }

    // Of course we need to increment time on each pass
    newTable->time += PHYLIB_SIM_RATE;
  }

  // Return our new copy of original table with newly updated/simulated values
  return newTable;
}

char *phylib_object_string(phylib_object *object) {
  static char string[80];
  if (object == NULL) {
    snprintf(string, 80, "NULL;");
    return string;
  }
  switch (object->type) {
  case PHYLIB_STILL_BALL:
    snprintf(string, 80, "STILL_BALL (%d,%6.1lf,%6.1lf)",
             object->obj.still_ball.number, object->obj.still_ball.pos.x,
             object->obj.still_ball.pos.y);
    break;
  case PHYLIB_ROLLING_BALL:
    snprintf(string, 80,
             "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
             object->obj.rolling_ball.number, object->obj.rolling_ball.pos.x,
             object->obj.rolling_ball.pos.y, object->obj.rolling_ball.vel.x,
             object->obj.rolling_ball.vel.y, object->obj.rolling_ball.acc.x,
             object->obj.rolling_ball.acc.y);
    break;
  case PHYLIB_HOLE:
    snprintf(string, 80, "HOLE (%6.1lf,%6.1lf)", object->obj.hole.pos.x,
             object->obj.hole.pos.y);
    break;
  case PHYLIB_HCUSHION:
    snprintf(string, 80, "HCUSHION (%6.1lf)", object->obj.hcushion.y);
    break;
  case PHYLIB_VCUSHION:
    snprintf(string, 80, "VCUSHION (%6.1lf)", object->obj.vcushion.x);
    break;
  }
  return string;
}
