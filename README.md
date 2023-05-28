# SocialNet


## Author

- Name: Abednego Emonena
- Email: emonenaabednego@gmail.com
- Twitter: @codynego

## Project Overview

SocialNet is an image sharing social network

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/codynego/SocialNet.git
   ```

2. Install the dependencies:

   ```shell
   pip install -r requirements.txt
   ```

3. Configure the database settings in `settings.py`.

4. Run database migrations:

   ```shell
   python manage.py migrate
   ```

5. Start the development server:

   ```shell
   python manage.py runserver
   ```

## API Endpoints

The following are the API endpoints available in this project:

### Authentication

- `POST api/auth/login/` - Log in to the system (auth_login_create)
- `POST api/auth/logout/` - Log out of the system (auth_logout_create)
- `PUT api/auth/password-reset/` - Update the user's password (auth_password-reset_update)
- `GET api/auth/password-reset/{uidb64}/{token}/` - Retrieve password reset details (auth_password-reset_read)
- `POST api/auth/register/` - Register a new user (auth_register_create)
- `POST api/auth/request-password-reset-email/` - Request a password reset email (auth_request-password-reset-email_create)
- `POST api/auth/resend-verification-email/` - Resend a verification email (auth_resend-verification-email_create)
- `POST api/auth/token/refresh/` - Refresh the access token (auth_token_refresh_create)
- `GET api/auth/verify-email/` - Verify the user's email (auth_verify-email_list)

### Hashtags

- `GET api/hashtags/` - Retrieve a list of all hashtags (hashtags_list)
- `GET api/hashtags/trending/` - Retrieve a list of trending hashtags (hashtags_trending_list)
- `POST api/hashtags/trending/` - Create a new trending hashtag (hashtags_trending_create)
- `GET api/hashtags/{id}/` - Retrieve details of a specific hashtag (hashtags_read)
- `PUT api/hashtags/{id}/` - Update a specific hashtag (hashtags_update)
- `PATCH api/hashtags/{id}/` - Partially update a specific hashtag (hashtags_partial_update)
- `DELETE api/hashtags/{id}/` - Delete a specific hashtag (hashtags_delete)

### Posts

- `GET api/posts/` - Retrieve a list of all posts (posts_list)
- `POST api/posts/` - Create a new post (posts_create)
- `GET api/posts/{id}/` - Retrieve details of a specific post (posts_read)
- `PUT api/posts/{id}/` - Update a specific post (posts_update)
- `PATCH api/posts/{id}/` - Partially update a specific post (posts_partial_update)
- `DELETE api/posts/{id}/` - Delete a specific post (posts_delete)
- `GET api/posts/{id}/comments/` - Retrieve comments for a specific post (posts_comments_list)
- `POST api/posts/{id}/comments/` - Create a new comment for a specific post (posts_comments_create)
- `DELETE api/posts/{post_id}/comments/{id}/` - Delete a specific comment for a specific post (posts_comments_delete)
- `POST api/posts/{post_id}/like/` - Like a specific post (posts_like_create)
- `DELETE api/posts/{post_id}/like/` - Unlike a specific post (posts_like_delete)

### Search

- `GET api/search/` - Search for users, hashtags, and posts (search_list)
- `GET api/search/hashtags/` - Search for hashtags (search_hashtags_list)
- `GET api/search/posts/` - Search for posts (search_posts_list)
- `GET api/search/users/`

### Timeline

- `GET api/timeline/` - Return the timeline of the authenticated user


## License

This project is licensed under the MIT License.