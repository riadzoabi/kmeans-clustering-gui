import customtkinter as ctk
from PIL import Image, ImageTk
import random
import math


def genNums():
    """Generate random points and insert them into the text area."""
    result_str = ""
    for i in range(100):
        num1 = random.uniform(1, 500)
        num2 = random.uniform(1, 350)
        formatted_numbers = f"{num1:.2f},{num2:.2f}\n"
        result_str += formatted_numbers
    text_area.insert(ctk.END, result_str)


def on_option_change(value):
    """Handle changes in the dropdown menu for selecting K."""
    global k
    k = int(value)
    print(f"Selected number: {k}")


def calcK():
    """Run the K-Means algorithm and plot the results."""
    canvas.delete("all")
    points_lines = text_area.get("1.0", ctk.END).strip().split("\n")
    points = []
    for line in points_lines:
        x, y = map(float, line.split(","))
        points.append([x, y])
    centroids, clusters = kmeans(points, k, 10000, 0.00000001)

    # Plot points
    colors = ["red", "green", "blue", "cyan", "magenta", "yellow", "black"]
    for j in range(len(clusters)):
        color = colors[j]
        for point in clusters[j]:
            x, y = point
            canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=color)
        for center in centroids:
            x, y = center
            canvas.create_oval(x - 6, y - 6, x + 6, y + 6, fill='black')


def euclid_dist(p, q):
    """Calculate the Euclidean distance between two points."""
    return math.sqrt(((q[0] - p[0]) ** 2) + ((q[1] - p[1]) ** 2))


def pickCenter(points, k):
    """Pick initial centroids randomly from the points."""
    seed = random.randint(0, 1000000)
    random.seed(seed)
    return random.sample(points, k)


def clusterize(points, centers):
    """Assign points to the nearest centroid to form clusters."""
    clusters = {}
    for point in points:
        distances = [euclid_dist(point, center) for center in centers]
        min_distance_index = distances.index(min(distances))
        if min_distance_index not in clusters:
            clusters[min_distance_index] = []
        clusters[min_distance_index].append(point)
    return clusters


def update_centroids(clusters):
    """Calculate new centroids from the clusters."""
    new_centroids = []
    for cluster in clusters.values():
        dimensions = len(cluster[0])
        centroid = [0] * dimensions
        for point in cluster:
            for i in range(dimensions):
                centroid[i] += point[i]
        centroid = [coord / len(cluster) for coord in centroid]
        new_centroids.append(centroid)
    return new_centroids


def has_converged(old_centroids, new_centroids, tolerance):
    """Check if the centroids have converged within the tolerance."""
    for i in range(len(old_centroids)):
        if (old_centroids[i][0] - new_centroids[i][0]) >= tolerance and (
                old_centroids[i][1] - new_centroids[i][1]) >= tolerance:
            return False
    return True


def kmeans(points, k, max_iterations, tolerance):
    """Perform the K-Means clustering algorithm."""
    centroids = pickCenter(points, k)
    for z in range(max_iterations):
        clusters = clusterize(points, centroids)
        new_centroids = update_centroids(clusters)
        if has_converged(centroids, new_centroids, tolerance):
            break
        centroids = new_centroids
    return centroids, clusters


def main():
    """Main function to set up and run the GUI application."""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    main_window = ctk.CTk()
    main_window.title("K Means Clustering")
    main_window.geometry("650x1000")
    main_window.resizable(False, False)

    # add logo
    image_path = "FireCluster@3x.png"  # Replace with your image path
    image = Image.open(image_path)
    ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(300, 180))
    label = ctk.CTkLabel(main_window, image=ctk_image, text="")
    label.pack(padx=10, pady=0)

    # Gen and enter points
    label2 = ctk.CTkLabel(main_window, text="Enter Points:")
    label2.pack()
    global text_area
    text_area = ctk.CTkTextbox(main_window, height=150, width=300)
    text_area.pack(pady=14)

    genPoints = ctk.CTkButton(main_window, text="Generate Random Points", command=genNums,
                              image=ctk.CTkImage(dark_image=Image.open("gen_icon.png").resize((32, 32))), compound="left")
    genPoints.pack(pady=14)

    # K-DropDown
    k_options = [2, 3, 4, 5]
    selected_option = ctk.StringVar()
    selected_option.set('K')
    label = ctk.CTkLabel(main_window, text="Choose Clusters num:")
    dropdown = ctk.CTkOptionMenu(main_window, variable=selected_option, values=[str(option) for option in k_options],
                                 command=on_option_change)
    label.pack()
    dropdown.pack(pady=14)

    # Run K means and plot
    button = ctk.CTkButton(main_window, text="Run K Means", command=calcK,
                           image=ctk.CTkImage(dark_image=Image.open("run_icon.png").resize((32, 32))), compound="left")
    button.pack(pady=14)

    # plot axis
    global canvas
    canvas = ctk.CTkCanvas(main_window, width=500, height=350, bg='white')
    canvas.pack(pady=14)

    credit = ctk.CTkLabel(main_window, text="Created by: The Amazing Riad Zoabi")
    credit.pack()

    main_window.mainloop()


if __name__ == "__main__":
    main()
