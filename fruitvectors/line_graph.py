import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from numpy import array
from concurrent.futures import ThreadPoolExecutor, wait
import fruitvectors


def line_graph(praw_client, search_filter=0):
    search_filter = get_limit(search_filter)
    fruit_vectors = fruitvectors.get_fruit_vectors(praw_client, search_filter)
    scores = []
    image_urls = []
    # Iterate through the list backwards
    for post_number in fruit_vectors[::-1]:
        current_fruit_vector = post_number
        try:
            image_urls.append(current_fruit_vector.url)
            scores.append(current_fruit_vector.score)
        # If a submission does not have an image, it is probably not useful
        except AttributeError:
            pass
    save_line_graph(scores, image_urls)


def get_limit(limit):
    if type(limit) == str:
        conversion_dict = {"week": 7, "month": 31}
        return conversion_dict[limit]
    return limit


def get_line_graph_images(urls: list):
    graph_size = [int((len(urls) * 120) * 1.75), int((len(urls) * 120) * 1.25)]
    futures = []
    pool = ThreadPoolExecutor()
    for url in urls:
        futures.append(pool.submit(scale_image, url, [100, 100], graph_size))
    wait(futures)
    images = []
    for future in futures:
        images.append(future.result())
    pool.shutdown()
    return [images, graph_size]


def scale_image(url: str, size: list, graph_size: list):
    image = fruitvectors.get_image(url, size)
    # If the image is over 3% of the total graph width or 4.7% of the total graph height, expand the graph
    if image.size[0] / graph_size[0] * 100 > 3 or image.size[1] / graph_size[1] * 100 > 4.7:
        graph_size[0] += 160
        graph_size[1] += 160
    image_array = array(image)
    return OffsetImage(image_array)


def save_line_graph(scores: list, urls: list):
    images, graph_size = get_line_graph_images(urls)
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
    vector_figure.savefig("./figure.png", bbox_inches="tight")
