# Look up a Course
 This looks up a specific course for a specific term at OSU to help you see which are still available and automatically submit them!
## How to use
 1. Download the files
 2. Open the terminal and navigate to the directory where you downloaded the files
 3. run the command `pip3 install -r requirements.txt`
 4. create a file and put the courses information you want:
    - The file should be a .txt file
    - The file should be in the format of 
    `1st line (courses), 2nd line (term (F,W,S)), 3rd line (times HH:MM-HH:MM(a/p)), 4th line (professors (first letter of first name. last name))`
    - MAKE SURE THERE IS NO SPACES AFTER THE COMMAS
    - Example: 
                CS261,CS162,CS290
                F
                10:00-10:50a,10:00-11:50a,1:00-1:50p
                Y.Song,A.Guyer,J.Coffman
    
 5. Set up .env file following .env.example
    - Ensure to have a valid OSU username and password
    - Also that your path has \\ instead of \ for windows
 6. To run the program there are two possible ways currently:
    - `python main.py search <Course> <Term> <Time> <Include_Online> <Professor> ` EACH MUST BE CAPS!!
        - Course: The course you want to look up
        - Term: The term you want to look up (F,W,S)
        - Time: The time you want to look up (HH:MM-HH:MM(a/p)) or SKIP
        - Include_Online: True or False
        - Professor: The professor you want to look up (first letter of first name. last name) or SKIP
            - Example: `python main.py search CS261 F 10:00-10:50a T Y.Song`
            - Example: `python main.py search CS261 W SKIP T SKIP`
    - `python main.py submit `
        - This will use the file you created to look up the courses
        - Example: `python main.py submit`
    - After running the submit option you will be prompted if you want to submit your schedule, currently it cannot pick the classes, but can submit the classes if you select them at https://classes.oregonstate.edu/. It currently goes until the last steps and asks you if you want to submit manually or automate it, I haven't been able to test this completely because I can't submit my schedule at this time, but I will when I can. If you want to submit manually, it'll give you 300 seconds to do what you please. 

 7. If at any point you want to close the program, just press ctrl+c


# Suggestions/Help

- If you want to help me out on this project feel free to, I'm not the best programmer, but I'm trying to learn and this is a project I've been wanting to do for a while.
- If you have any suggestions on how to improve the program, please let me know!
- You can reach me at discord at: `eclinick`
 
