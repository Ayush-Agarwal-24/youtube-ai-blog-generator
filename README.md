 # YouTube AI Blog Generator

 This Django web application allows users to create blog posts automatically by extracting transcriptions from YouTube videos and transforming them into comprehensive blog articles using OpenAI's GPT models. It's designed for content creators who want to repurpose video content into written form.

 ## Features

 - **User Authentication**: Secure login, signup, and logout functionalities.
 - **YouTube Video Transcription**: Automatically transcribe audio from YouTube videos.
 - **Blog Post Generation**: Utilize AI to convert transcriptions into well-structured blog posts.
 - **Blog Management**: Users can view and manage their generated blog posts.

    ![Login Page](https://github.com/Ayush-Agarwal-24/youtube-ai-blog-generator/blob/main/screenshots/Screenshot%20(113).png)
    ![Signup Page](https://github.com/Ayush-Agarwal-24/youtube-ai-blog-generator/blob/main/screenshots/Screenshot%202024-06-05%20143456.png)
    ![Index Page](https://github.com/Ayush-Agarwal-24/youtube-ai-blog-generator/blob/main/screenshots/Screenshot%202024-06-05%20143536.png)
    ![Youtube Link Added](https://github.com/Ayush-Agarwal-24/youtube-ai-blog-generator/blob/main/screenshots/Screenshot%202024-06-05%20143737.png)
    ![Generated Blog Article](https://github.com/Ayush-Agarwal-24/youtube-ai-blog-generator/blob/main/screenshots/Screenshot%202024-06-05%20143851.png)
    ![All Saved Blog Posts](https://github.com/Ayush-Agarwal-24/youtube-ai-blog-generator/blob/main/screenshots/Screenshot%202024-06-05%20143919.png)
    ![Blog Post Details](https://github.com/Ayush-Agarwal-24/youtube-ai-blog-generator/blob/main/screenshots/Screenshot%202024-06-05%20144000.png)


 ## Prerequisites

 Before you begin, ensure you have met the following requirements:
 - Python 3.8 or higher
 - Django 3.2 or higher
 - PostgreSQL
 - An API key from OpenAI
 - An API key from AssemblyAI for transcription

 ## Installation

 1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Ayush-Agarwal-24/youtube-ai-blog-generator.git


 2 Set Up a Virtual Environment (optional but recommended):

    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

 3 Install Required Packages:

    pip install -r requirements.txt

 4 Environment Setup: Create a .env file in the project root directory and fill it with your credentials:

    DATABASE_NAME=your_database_name
    DATABASE_USER=your_database_user
    DATABASE_PASSWORD=your_database_password
    DATABASE_HOST=localhost
    DATABASE_PORT=5432
    OPENAI_API_KEY=your_openai_api_key
    AAI_API_KEY=your_assemblyai_api_key

 5 Database Migrations:

    python manage.py migrate

 6 Run the Development Server:

    python manage.py runserver

 7 Access the Application: Open your web browser and go to http://127.0.0.1:8000.


## Usage

 • Home Page: Accessible at /. You need to login to use the features.
 
 • User Authentication: Use /login for login, /signup for registration, and /logout to log out.
 
 • Generating Blog Posts: After logging in, submit a YouTube link to generate a blog. The application will handle
   transcription and blog post generation.
   
 • View Blogs: Navigate to /blogs to see all generated blog posts.
 
 • Blog Details: Click on any blog post to view its details.


## Contributing

Contributions to this project are welcome! If you have suggestions or improvements, please fork the repository and
create a pull request or open an issue with the tag "enhancement". Don't forget to give the project a star!


## License

This project is licensed under the MIT License - see the LICENSE.md file for details.


## Contact

For support or queries, reach out to me at ayushagarwal1226@gmail.com.
