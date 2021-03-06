import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from numpy import array
from concurrent.futures import ThreadPoolExecutor, wait
import fruitvectors


def line_graph(praw_client, start_limit=0, end_limit=-1, recent=True):
    fruit_vectors = fruitvectors.get_fruit_vectors(praw_client, recent, start_limit, end_limit)
    scores, image_urls = fruitvectors.get_scores_and_urls(fruit_vectors)
    _save_line_graph(scores, image_urls)


def _get_line_graph_images(urls: list):
    graph_size = [int((len(urls) * 120) * 1.75), int((len(urls) * 120) * 1.25)]
    futures = []
    pool = ThreadPoolExecutor()
    for url in urls:
        futures.append(pool.submit(_scale_image, url, [100, 100], graph_size))
    wait(futures)
    images = []
    for future in futures:
        images.append(future.result())
    pool.shutdown()
    return [images, graph_size]


def _scale_image(url: str, size: list, graph_size: list):
    image = fruitvectors.get_image(url, size)
    # If the image is over 3% of the total graph width or 4.7% of the total graph height, expand the graph
    if image.size[0] / graph_size[0] * 100 > 3 or image.size[1] / graph_size[1] * 100 > 4.7:
        graph_size[0] += 160
        graph_size[1] += 160
    image_array = array(image)
    return OffsetImage(image_array)


def _save_line_graph(scores: list, urls: list):
    images, graph_size = _get_line_graph_images(urls)
    size = graph_size[0]/100
    vector_figure = plt.figure(figsize=[graph_size[0]/100, graph_size[1]/100])
    axes = plt.axes()
    axes.set_title("Fruit Vectors", size=size*3)
    axes.set_ylabel("Score", size=size*3)
    axes.set_xlabel("Day", size=size*3)
    plt.setp(axes.get_xticklabels(), size=size*2)
    plt.setp(axes.get_yticklabels(), size=size*2)
    axes.plot(scores, color="black", marker="o", markerfacecolor="red", linewidth=5)
    count = 0
    for score in scores:
        ab = AnnotationBbox(images[count], (count, score), frameon=False)
        axes.add_artist(ab)
        count += 1
    vector_figure.add_axes(axes)
    vector_figure.savefig("./line.png", bbox_inches="tight")
