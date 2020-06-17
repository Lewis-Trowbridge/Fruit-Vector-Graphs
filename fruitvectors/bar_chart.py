import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from numpy import array
from concurrent.futures import ThreadPoolExecutor, wait
import fruitvectors


def bar_chart(praw_client, start_limit=0, end_limit=-1, recent=True):
    fruit_vectors = fruitvectors.get_fruit_vectors(praw_client, recent, start_limit, end_limit)
    scores, image_urls = fruitvectors.get_scores_and_urls(fruit_vectors)
    _save_bar_chart(scores, image_urls)


def _save_bar_chart(scores: list, urls: list):
    score_nums = []
    for score_num in range(1, len(scores)+1):
        score_nums.append(str(score_num))
    vector_figure = plt.figure(figsize=[19.2, 10.8])
    axes = plt.axes()
    axes.set_title("Fruit Vectors")
    bars = plt.bar(score_nums, scores)
    axes.bar = bars
    vector_figure.add_axes(axes)
    vector_figure.savefig("./bar.png")
