import requests
from PIL import Image
import praw

# The IDs of the currently known subreddits these are posted on
whitelisted_subreddit_ids = ["t5_2qjpg", "t5_2qi1r", "t5_2vegg", "t5_2zmfe"]


def get_fruit_vectors(fruit_vector_client: praw.Reddit, limit: int):
    posts = fruit_vector_client.redditor("ErmineDev").submissions.new(limit=300)
    fruit_vectors = []
    count = 1
    for current_post in posts:
        if current_post.subreddit_id in whitelisted_subreddit_ids:
            # The ID of the first non-fruit vector post, stop here if this is also the current post ID
            if current_post.id != "eos9jv" and (count < limit + 1 or limit == 0):
                fruit_vectors.append(current_post)
            else:
                break
            count += 1
    return fruit_vectors


def get_image(url: str, size: list):
    image_request = requests.get(url, stream=True)
    temp_image = Image.open(image_request.raw)
    temp_image = temp_image.resize((size[0], size[1]), Image.BICUBIC)
    return temp_image
