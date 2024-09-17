# Personal Assistant Appointment System

This is a personal assistant appointment system built using Streamlit, LangChain, and Zapier. It allows users to schedule service appointments with Sanchuka, a software engineer who offers solution consulting, full-stack development, and AI/ML development services.

## Features

- Chat interface for scheduling appointments
- Collects user details including full name, service type, location, datetime, and email address
- Saves chat history and allows deletion through the sidebar
- Integration with Zapier for additional functionalities

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your API keys:
    ```
    OPENAI_API_KEY=your_openai_api_key
    ZAPIER_NLA_API_KEY=your_zapier_nla_api_key
    ```

5. Run the Streamlit app:
    ```bash
    streamlit run main.py
    ```

## Usage

- Open the Streamlit app in your browser.
- Interact with the chat interface to schedule an appointment.
- View and manage the chat history from the sidebar.

## Contributing

Feel free to submit issues and pull requests. For any questions or suggestions, please open an issue on GitHub.

## License

This project is licensed under the MIT License.
