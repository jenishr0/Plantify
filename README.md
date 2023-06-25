Household Plants E-commerce App

This app is a household plants e-commerce platform that allows users to browse through plants available on the website and purchase them. It is built with Python and Flask and utilizes an external API to display plant descriptions and prices. Users can create an account to store their personal details and purchase history. The app is containerized with Docker and deployed using Kubernetes for efficient and scalable management.

Table of Contents
Installation
Usage
Technologies Used
Contributing
License
Installation

To use this app, you will need to have Docker and Kubernetes installed on your machine. Clone this repository and navigate to the root directory.

To build the Docker image, run the following command:

Bash
docker build . -t <image-name>


To deploy the app using Kubernetes, first apply the necessary Kubernetes configurations in the kubernetes directory:

Bash
kubectl apply -f kubernetes


Once all the configurations have been applied successfully, the app should be up and running.

Usage

To use the app, navigate to the URL where it is deployed. You can browse through the different plants available and add them to your cart. Create an account to store your personal details and purchase history. Once you are ready to make a purchase, checkout and make the payment.

Technologies Used
Python
Flask
Docker
Kubernetes
External API
Contributing

If you would like to contribute to this app, please follow these steps:

Fork this repository
Create a new branch (git checkout -b feature/<feature-name>)
Make your changes and commit them (git commit -m "Add feature")
Push your changes to your forked repository (git push origin feature/<feature-name>)
Open a pull request
License

This project is licensed under the MIT License. See the LICENSE file for more information.
