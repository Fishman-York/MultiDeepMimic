# Manual

## How to run the code

Install the dependencies according to the readme.

Assuming that everything is running fine, we can now create an argument file to run our code. Example argument files are in the DeepMimic source code. In particular, I have edited play_2_char.txt, play_motion_humanoid3d_args.txt and train_char.txt. The other files are from DeepMimic, which I have left in as examples. However, do note to follow the convention from the 3 files I have outlined.

If you want to create your own files, I have listed the convention needed in my dissertation, in the appendix. However, you can also extrapolate it from the example files I have listed above. Those files contain everything that I have focused on in this project. If you get a segmentation fault, it is most probably because something you edited in the argument files went wrong.

How do we run these argument files?

If you want to display a motion clip:

python DeepMimic.py --arg_file args/play_motion_humanoid3d_args.txt

If you want to play a different argument file:

python DeepMimic.py --arg_file file/path

Do note that this just displays the mocap data you have put in. It does not take into account physics, just the rotation of the joints from the root.

Simulations that run pre-trained policies are also similar in how they are run.

python DeepMimic.py --arg_file args/play_2_char.txt

You will notice that it still uses DeepMimic.py. The difference here is the arg file.

Training a policy is different, however.

python mpi_run.py --arg_file args/train_char.txt --num_workers 16

You will notice that this uses mpi_run to initialise a number of instances. You can customise it by changing the num_workers field.

python mpi_run.py --arg_file args/train_char.txt --num_workers i

Just change i to any integer, as long as your CPU cores allow it. Usually the amount of CPU cores you have influence the number of workers you can deploy. Also, do not go above 16 as that will overwhelm DeepMimic.

## Argument Files
Argument Files are where it starts to get complicated. If you want to train your own policy, follow the train_char argument txt file that I edited. A documentation for convention is also in my dissertation. In general, for those marked with M, if you want multiple characters, the number of arguments in the fields marked as M have to correspond to the amount of characters.

If you train your own policy to see how 2 characters interact, I would advise you to first train them separately. This allows them to create their own individual policy. After that, you can train them together, using their individual policy files to speed up the good results. How you do this is specifying the argument --model_files in the training argument file, similar to how you run a pre trained policy. However, if you want to start a fresh policy, delete the --model_files field entirely, or it will throw an error.

If you want your computer to take a break, you can stop the simulation with ctrl+c, but do note that deepmimic is not exactly made to do this. A sort of workaround is to use model files of the output that you have produced from your paused session, but this does affect results slightly. A continuous run is best for consistent results.

## Runtime
That being said, DeepMimic takes very long to run. The author has said that simple motions of a singular character needs at least 60000000 samples to be stable. In a day, with 16 workers, I was able to produce that amount. This means that more complex motions (particularly 2 characters) would need more time. In general, though, I did receive good results after running it for that amount.

## Conversion Scripts

If you want to create your own dataset, you can take a look in the python files left in the conversion folder. I used conversion.py to alter CHI3D sets, which didn't really work. This is due to the misconception I had with rotation matrixes. You can instead use rotate_deepmimic.py to flip a motion file from DeepMimic around, to simulate two characters interacting. Just alter the variables left at the top and run main().

## Output of Agent Data
Output of agent logs, as well as cpkt, are all put in the output file as per the argument files. Looking at the output file, it's in a kind of CSV table format that is very hard to look at. You can use convert_log.py in the conversion folder to get a readable output of the last commited information for the agents.

