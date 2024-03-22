# START HACK 2024 - Cisco Spaces Challenge - Solution Team notime

The Challenge can be found here: [Cisco_STARTHACK24](https://github.com/START-Hack/Cisco_STARTHACK24/tree/main)


## Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Installation (Linux/Mac)

1. Clone this repository

2. Build the Docker containers
    ```bash
    $ docker compose up --build
    ```

3. Accessing the Services
    - **Traefik Dashboard** <br> https://127.0.0.1/traefik
    - **Backend Swagger API** <br> https://127.0.0.1/backend/api/doc/


## Who are we?
 - *Lukas Goldschmidt* [LinkedIn Profile](https://www.linkedin.com/in/lukas-goldschmidt/)
 - *Niklas Keller*
 - *Leon Schmidt*
 - *Moritz Valerius* [LinkedIn Profile](https://www.linkedin.com/in/moritzvalerius/)

    
## Problem description & relevance
Visually impaired people have great difficulty navigating through crowded aisles in supermarkets to find certain products. Even if they have managed this route, they often cannot manage the last few meters on their own. Am I holding the milk with 1.5% fat or 3.5% fat in my hand?

These people are dependent on the help of others. It is clear that in many cases this does not work satisfactorily and is very restrictive for the person with a disability.

More than 250 million people worldwide are affected by visual impairment. This can vary in severity. It can range from extreme nearsightedness, to being able to see contrasts only, to total darkness. But they all share the same problem. 

## Outline the solution with Cisco
The core technology of this solution consists of determining the location within the building. The location data provided by the Cisco Firehouse API is fused with sensor data from the smartphone (gyroscope, compass) in order to determine a relatively precise position within the building.

The necessary technologies are available. Our solution is divided into four approaches.

1. supermarkets have precise location data for each of their products. This was verified by us in a conversation with a manager of an internationally operating supermarket chain based in Germany.

2. the mobile phone as a technical device can be tracked to within a few metres thanks to the spatial positioning of CISCO devices within a supermarket. We have verified and visualised the quality of the data. -> (.res/*.png)

3. sensors in the same mobile phone can greatly improve this CISCO data and, in our case, further reduce the spatial positioning of a few metres. The location data provided by the Cisco Firehouse API is fused with sensor data from the smartphone (gyroscope, compass) with the position (for example using Kalman filters).

4. machine learning enables targeted recognition and guidance of the mobile phone to the product being searched for.   

## Our prototype
But see for yourself. Here is a video showing how our prototype guides a visually impaired person through a supermarket to the milk carton he is looking for (Video - StartHack24.mp4). 

The CISCO devices know the spatial structure of the supermarket and can determine the location of the blind person. 

By connecting to the supermarket's system, the position of the product they are looking for can be determined in the store's three-dimensional coordinate system. 

Using the sensors in the mobile phone, the visually impaired person is guided along the marked path. If they turn in the wrong direction, they are acoustically guided back to the correct path.

When they arrive at the shelf, the phone scans the shelves and accurately marks the product to be picked up. The visually impaired person is guided to the product by the phone's vibration pattern and can pick it up.

## Technical background

### OCR-based Product Recognition from Price Tags:
The implementation of optical character recognition (OCR) for identifying products through price tags was not included in the prototype primarily due to time constraints. However, integrating an OCR library or API, such as Tesseract, into the application could facilitate this feature. By training the OCR system to recognize characters on price tags, the application would be able to identify products on shelves based on their price labels.

### Localization of Products through Supermarket Inventory System Integration
The integration with the supermarket's inventory system to localize products in real-time was not implemented within the prototype due to the lack of an interface with an existing supermarket inventory system. However, a suggested approach would involve developing an interface to connect with the supermarket's inventory database using APIs or web scraping techniques. This would enable the application to retrieve up-to-date information about the location of products within the store, thus providing accurate navigation guidance for users.

### Simulation of User's Positional Data
Due to the unavailability of real-time positional data, the prototype utilized simulated positional data of the user within the building. This simulated data allowed the application to demonstrate navigation functionality within the indoor environment. While not reflective of actual user positions, this approach served to illustrate how the application could guide individuals to desired products within a store setting. Integrating with real-time positioning systems in future iterations would enhance the accuracy and effectiveness of the navigation feature.
