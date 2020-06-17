import requests
from PIL import Image
import praw

# The IDs of the currently known subreddits these are posted on
whitelisted_subreddit_ids = ["t5_2qjpg", "t5_2qi1r", "t5_2vegg", "t5_2zmfe"]


def get_fruit_vectors(fruit_vector_client: praw.Reddit, recent: bool, start_limit=0, end_limit=-1):
    posts = fruit_vector_client.redditor("ErmineDev").submissions.new(limit=300)
    fruit_vectors = []
    for current_post in posts:
        if current_post.subreddit_id in whitelisted_subreddit_ids:
            # The ID of the first non-fruit vector post, stop here if this is also the current post ID
            if current_post.id != "eos9jv":
                fruit_vectors.append(current_post)
            else:
                break
    if start_limit > len(fruit_vectors):
        start_limit = 0
    if end_limit < start_limit:
        end_limit = len(fruit_vectors)
    if recent:
        return fruit_vectors[start_limit:end_limit][::-1]
    elif not recent:
        return fruit_vectors[::-1][start_limit:end_limit]


def get_scores_and_urls(fruit_vectors: list):
    scores = []
    image_urls = []
    # Iterate through the list and get image URLS and scores
    for post_number in fruit_vectors:
        current_fruit_vector = post_number
        try:
            image_urls.append(current_fruit_vector.url)
            scores.append(current_fruit_vector.score)
            # If a submission does not have an image, it is probably not useful
        except AttributeError:
            pass
    return [scores, image_urls]


def get_image(url: str, size: list):
    image_request = requests.get(url, stream=True)
    temp_image = Image.open(image_request.raw)
    temp_image = temp_image.resize((size[0], size[1]), Image.BICUBIC)
    return temp_image
