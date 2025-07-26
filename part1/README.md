HBNB-EVOLUTION-DOCS         
                            
                            HBnB Project Manual        

NAME
       hbnb-evolution-docs - Technical Documentation for the HBnB Evolution Project

SYNOPSIS
       Architecture | Business Logic | API Interaction Flow

DESCRIPTION
       This document provides the complete technical documentation for the HBnB
       Evolution project, an application inspired by AirBnB. Its purpose is to
       serve as a foundational blueprint and detailed guide for the development
       and implementation phases of the system.

       The content covers the high-level architecture, the detailed design of
       the business logic, and the interaction flows for API calls. This
       documentation ensures a solid understanding of the application's design
       and architecture, facilitating a coherent and structured development
       process.

ARCHITECTURE (TASK 0)
       The following diagram and explanatory notes describe the application's
       three-layer architecture, which ensures a clear separation of concerns
       and improves system maintainability.

   1.1. Package Diagram
   
   ![diagrama1 (1)](https://github.com/user-attachments/assets/01b2e99c-f9d5-4eca-b832-7ee140a96613)

   1.2. Explanatory Notes
       Presentation Layer
              This layer is the entry point for all client interactions. It
              includes the API and services that expose the system's
              functionality to the outside world.

       Business Logic Layer
              This layer contains the application's core logic and business
              entities. The models for USER, PLACE, REVIEW, and AMENITY are
              defined here.

       Persistence Layer
              This layer is responsible for all communication with the
              database, including data storage and retrieval.

       Facade Pattern
              This design pattern is used as an intermediary between the
              Presentation Layer and the Business Logic Layer. It provides a
              unified and simplified interface to a more complex set of
              subsystems in the business logic, decoupling the layers and
              organizing the communication flow.

BUSINESS LOGIC LAYER (TASK 1)
       This diagram details the classes within the Business Logic Layer, their
       attributes, methods, and the relationships between them.

   2.1. Class Diagram
   ![image](https://github.com/user-attachments/assets/9de34399-cb4c-4fe2-ae64-7d2c5cc84ab2)

   2.2. Explanatory Notes
       BaseEntity (Abstract)
              An abstract class that serves as a base for other entities. It
              provides common audit fields like `createdAt` and `updatedAt`.

       User
              Represents system users.
              - Attributes: `firstName`, `lastName`, `email`, `password`, and
                a boolean `isAdmin`.
              - Methods: Key functionalities like `register()`, `updateProfile()`,
                `authenticate()`, and `delete()`.
              - Relationships: A User can write multiple Reviews and owns
                multiple Places.

       Place
              Represents a property listed in the application.
              - Attributes: `title`, `description`, `pricePerNight`, `latitude`,
                `longitude`, and `ownerId`.
              - Methods: Allows operations like `create()`, `update()`, `delete()`,
                and `addAmenity()`.
              - Relationships: Associated with one User (the owner), receives
                multiple Reviews, and has multiple Amenities.

       Review
              Represents a user's review of a place.
              - Attributes: `rating` (Integer), `comment` (String), `userId`,
                and `placeId`.
              - Methods: Supports `create()`, `update()`, and `delete()`
                operations.
              - Relationships: Each Review is written by one User and is
                associated with one Place.

       Amenity
              Represents a service or feature a place can offer.
              - Attributes: `name` and `description`.
              - Methods: Includes `create()`, `update()`, and `delete()`.
              - Relationships: An Amenity can be associated with multiple Places.

API INTERACTION FLOW (TASK 2)
       The following sequence diagrams illustrate the flow of interactions
       between layers for four key API calls.

   3.1. User Registration (`POST /api/users`)
       This diagram shows the process of registering a new user.
       
       ![image](https://github.com/user-attachments/assets/cdf9a7f0-c059-45ca-aec9-f72945faf819)

       1. The Client sends a `POST` request to the API with user data.
       2. The Presentation Layer (API) validates the input. If invalid, it
          responds with `400 Bad Request`.
       3. If valid, the API invokes the Business Logic Layer to create the user.
       4. The Business Logic Layer hashes the password and requests the
          Persistence Layer to check if the email already exists.
       5. If the email exists, an error is returned, and the API responds with
          `409 Conflict`.
       6. If the email does not exist, the Persistence Layer saves the new
          user and returns a confirmation.
       7. The API responds to the Client with `201 Created`.

   3.2. Place Creation (`POST /api/places`)
       This diagram illustrates how an authenticated user lists a new place.
       
       ![image (1)](https://github.com/user-attachments/assets/859a5f2f-2ff4-4898-ab0f-af377bddc643)
       

       1. The Client sends a `POST` request with the place data.
       2. The Presentation Layer (API) validates the data. If invalid, it
          responds with `400 Bad Request`.
       3. If valid, it invokes `createPlace(placeData)` in the Business Logic
          Layer.
       4. The Business Logic Layer requests the Persistence Layer to save the new
          place.
       5. After confirmation, the API responds to the Client with `201 Created`.

   3.3. Review Submission (`POST /api/reviews`)
       This diagram shows the flow for a user to post a review for a place.
       ![image (2)](https://github.com/user-attachments/assets/c5bc2195-6c7b-4610-95d7-137d9fd8f6b7)
       

       1. The Client sends a `POST` request with review data.
       2. The Presentation Layer (API) validates the data. If invalid, it returns
          `400 Bad Request`.
       3. If valid, it invokes `createReview` in the Business Logic Layer.
       4. The Business Logic Layer requests the Persistence Layer to save the
          new review (`Save review`).
       5. After confirmation, the Business Logic Layer requests the Persistence
          Layer to update the place's average rating (`Update place rating`).
       6. The API responds to the Client with `201 Created`.

   3.4. Fetching a List of Places (`GET /api/places`)
       This diagram describes how a list of places is retrieved.
       
       ![image (3)](https://github.com/user-attachments/assets/53194610-3cd9-4f89-b963-117d0e3a7380)
       

       1. The Client sends a `GET /api/places` request, optionally with filters.
       2. The Presentation Layer (API) parses the filter parameters.
       3. It invokes `getPlaces(filters)` in the Business Logic Layer.
       4. The Business Logic Layer requests the Persistence Layer to perform a
          query based on the filters (`Query places`).
       5. The Persistence Layer returns the results.
       6. The Business Logic Layer processes the results and returns them to
          the Presentation Layer.
       7. The API responds to the Client with `200 OK` and the place data.

REPOSITORY
       GitHub Repository: holbertonschool-hbnb
       Directory:         part1

AUTHOR
       Written by the HBnB Evolution Project Team. ARÉVALO, Alejandro; CABRERA, Nahuel; ROMERO, Emmanuel
       https://www.canva.com/design/DAGpfUrJxKo/L0_rbOM893847rZDCDUI-A/edit?utm_content=DAGpfUrJxKo&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

HBNB Evolution Project
