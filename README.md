\# Game of Sickness\
\
Game of Sickness is a simulation of the spread of an infection based on
Conway\'s Game of Life. This project is created as a school assignment
to illustrate how various parameters affect the spread of an infection,
recovery, and mortality rates.\
\
\## Installation\
\
To run this project, you need to have Python installed along with the
required packages listed in \`requirements.txt\`. You can install the
required packages using pip:\
\
\`\`\`bash\
pip install -r requirements.txt\
\
**Running the Game**\
To start the game, run the following command:\
python game_of_sickness.py\
**Game Controls**

-   Infectiousness Slider: Adjusts the probability of an infection
    spreading from an infected cell to a neighboring cell.

-   **Recovery Chance Slider**: Adjusts the probability of an infected
    cell recovering.

-   **Mortality Rate Slider**: Adjusts the probability of an infected
    cell dying.

-   **Birth Chance Slider**: Adjusts the probability of a new cell being
    born.

-   **Mutation Rate Slider**: Adjusts the probability of a recovered
    cell getting re-infected.

-   **Restart Button**: Resets the game with the current parameters.

-   **Stop Button**: Pauses the game and saves the infection wave plot.

-   **Waves Button**: Activates the infection waves mode, where the
    mutation rate and recovery chance vary over time.

-   **Vaccine Button**: Activates the vaccine mode, where the recovery
    chance gradually increases.\
    \
    **Project Description**\
    This project is developed as a school assignment. It simulates the
    spread of an infection using cellular automata principles. The game
    allows users to adjust various parameters and observe how they
    impact the infection dynamics.\
    **License**\
    This project is licensed under the MIT License. See the LICENSE file
    for details.
