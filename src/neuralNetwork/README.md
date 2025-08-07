# Input normalization

I won't input the distances in pixels, as these are too large numbers. There would have to be a big numerical drop in each layer, or use high values up to the output layer. That's mess.

Each input to the newtork will range from 0 to 1.

## X normalization

The X normalization works by dividing the distance by 193 (distance between pipes) so it ranges from 0 to 1 (1 is far, 0 is near).

PS: at startup the distance is more than 1 (439 pixels - 2.27).

## Y normalization

The ideal Y normalization would be from -1 to 1; at -1 the bird is way below the gap, at 1 it is way above the gap and 0 is aligned with it. In the final network, there maybe could be negative inputs. But as I haven't researched about them yet:

The Y normalization also converts the distance from 0 to 1, but in a different logic. 0 is way below the gap and 1 is way above the gap. 0.5 is aligned with the gap (the bird must stay as close as possible to 0.5).

We'll see (and I have to study about this) if this shrink and offset of the range (from [-1; 1] to [0; 1]) will prevent the network from learning.