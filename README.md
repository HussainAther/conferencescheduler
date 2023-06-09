Great! Here's the updated README.md file with the GUI improvements:

```markdown
# (Optional) API Mock Technical Assessment
## Conference Scheduler

The goal of this assessment is to create a program that interacts with an API endpoint to retrieve conference data, organize the data, and post a schedule back to the same endpoint. The program is implemented using object-oriented programming (OOP) principles.

## Prerequisites

Before running the program, make sure to install `requests-cache` by executing the following command:

```bash
pip install requests-cache
```

## Files

The assessment consists of the following files:

1. `program.py`: This file contains the implementation of the ConferenceScheduler class and its dependencies. It includes methods for making API calls, creating schedules, and posting schedules back to the API endpoint. The file also includes a Conference class to represent individual conferences. Error handling is implemented for handling exceptions during API calls and schedule creation.

2. `unittests.py`: This file contains unit tests for verifying the functionality of the methods and classes in `program.py`. The unit tests cover different scenarios, such as successful API calls, handling API errors, and verifying the correctness of schedule creation and posting.

3. `README.md`: This file provides instructions and information about the assessment.

## Usage

To use the program, follow these steps:

1. Install the required `requests-cache` library by running the command mentioned above.

2. Open a terminal or command prompt and navigate to the directory containing the program files.

3. Run the command `python program.py` to execute the program.

    - The program will open a GUI window that displays a label and a "Fetch Data" button.

    - Click the "Fetch Data" button to make an API call and fetch conference data from the specified API endpoint.

    - The program will process the data, create a schedule based on the available dates of the conference partners, and store the schedule in memory.

    - If the fetching and schedule creation process is successful, a success message will be displayed in the GUI window.

4. To stop the program at any time, click the "Stop" button in the GUI window.

5. To run the unit tests, execute the command `python unittests.py` in the terminal or command prompt.

    - The unit tests will validate the functionality of the methods and classes in `program.py`. Each test case will verify a specific aspect of the program's behavior, such as successful API calls, error handling, and correct schedule creation and posting.

    - The unit tests will provide feedback on whether the program functions as expected and help identify any issues or errors.

## Conclusion

The Conference Scheduler program demonstrates the use of object-oriented programming to interact with an API, organize data, and perform actions such as creating and posting schedules. The unit tests provide confidence in the correctness of the program's functionality and help ensure its robustness.

By successfully completing the assessment and receiving a status code of 200 upon posting the schedule, you have achieved the desired outcome of the assignment.

## Authors
Syed Hussain Ather
```

Please make sure to update the author name and any additional information as needed.