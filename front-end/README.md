# Frontend Project Structure Guide
## Overview
Welcome to the frontend project structure guide for the Comrade Marketplace e-commerce website. This document aims to provide a clear understanding of the project's directory structure, organization, and the purpose of each directory and file. This guide will help you navigate the project effectively and collaborate efficiently with your team members.

## Directory Structure
```markdown
Copy code
/src
  /assets
    - Contains static assets such as images and stylesheets.
  /components
    - Contains reusable UI components organized by functionality.
    - /common: Contains common layout components like Header and Footer.
    - /product: Contains components related to displaying product information.
    - /cart: Contains components related to managing the shopping cart.
    - /auth: Contains components for user authentication and registration.
  /contexts
    - Contains React context providers managing global state.
    - AuthContext.tsx: Manages user authentication state.
    - CartContext.tsx: Manages shopping cart state.
  /pages
    - Contains higher-level components representing different pages/routes of the application.
    - Home.tsx: Home page component.
    - Products.tsx: Products listing page component.
    - ProductDetailPage.tsx: Product detail page component.
    - CartPage.tsx: Shopping cart page component.
    - CheckoutPage.tsx: Checkout page component.
  /services
    - Contains service modules handling API requests and authentication.
    - api.ts: Functions for making API requests to the backend.
    - auth.ts: Functions for handling user authentication.
  /styles
    - Contains global stylesheets and variables.
    - global.css: Global styles that apply to the entire application.
    - variables.css: CSS variables for consistent theming and styling.
/App.tsx
  - Root component of the application where routing and global providers are typically set up.
/index.tsx
  - Entry point of the application where React is initialized and the root component is rendered.
```
## Guide
- /assets:<br/>
This directory is dedicated to storing static assets such as images and stylesheets used throughout the application.

- /components:<br/>
Contains reusable UI components organized by functionality. Each subdirectory represents a specific category of components, making it easier to locate and reuse components across the application.

- /contexts:<br/>
Houses React context providers managing global state. These contexts are essential for managing user authentication and the shopping cart state across multiple components.

- /pages:<br/>
Contains higher-level components representing different pages or routes of the application. Each page component corresponds to a specific URL route and encapsulates the logic and UI for that particular page.

- /services:<br/>
Contains service modules responsible for handling API requests and authentication. These services abstract away the implementation details of interacting with external APIs, promoting separation of concerns and reusability.

- /styles:<br/>
Stores global stylesheets and variables used for consistent styling and theming across the application. Global stylesheets define the overall look and feel of the application, while variables provide flexibility and maintainability.

- App.tsx: <br/>
The root component of the application where routing and global providers are typically set up. This component serves as the entry point for rendering the application and orchestrating the overall application logic.

- index.tsx:<br/>
The entry point of the application where React is initialized and the root component is rendered. This file bootstraps the React application and mounts it to the DOM.

## Conclusion
This frontend project structure is designed to promote modularity, reusability, and maintainability, enabling efficient development and collaboration among team members.<br/>
By adhering to this structure and understanding the purpose of each directory and file, you can navigate the project effectively and contribute to its success.

If you have any questions or need further clarification on any aspect of the project structure, feel free to reach out to the team lead or refer to the project documentation.

Happy coding!
=======
# GDSC Kabarak University Comrade MArketplace Frontend
***
This repository contains the React frontend for GDSC Kabarak University Comrade Marketplace project, which is an e-commerce platform for membres of GDSC community. The frontend provides an interface for users to interact with the platform, browse products,and make puchases.

## Specifications
- REACT 17.0.1
- React Router 5.2.0

## Requirements
- Node.js (version 14 or later)
- npm (version 6 or later)

## Setup
1. Clone the repository:
``` 
git clone https://github.com/DSCKabarak/ComradeMarketPlace 
```

2. Change Directory to `front-end`:
``` 
cd front-end
```

3. Install dependencies:
``` 
npm install
```

4. Start the development server:
``` 
npm start
```

The development server should be now running on `http://localhost:3000`

## Contributing
We welcome Kabarak Developers contributors to the community! If you'd like to contribute to the frontend project, please follow these steps: <br/>

1. Folk the repository
2. Create a new branch for your changes
3. Make your changes and commit them
4. Push your changes to the folkrd repository
5. Submit a pull request to the main repository <br/>

Before submitting a pull request, please make sure that your code is well-documented, please follow the projects' coding standards, and include tests where applicable.

## Folder Structure
```
comrade-marketplace/
├── public/
│   ├── index.html
│   └── ...
├── src/
│   ├── api/
│   │   ├── index.js
│   │   └── ...
│   ├── components/
│   │   ├── Navbar/
│   │   │   ├── ...
│   │   │   └── ...
│   │   └── ...
│   ├── pages/
│   │   ├── Home/
│   │   │   ├── ...
│   │   │   └── ...
│   │   └── ...
│   ├── App.js
│   ├── index.js
│   └── ...
├── .gitignore
├── package.json
└── README.md
```

- `public/`: Contains the public assets for theproject, such as HTML file and assets.
- `api/`: Contains the API module for backend communication.
- `components/`: Contains the reusable UI components for the project.
- `pages/`: Contains the top-level pages for the project.
- `App.js`: The root component of the application.
- `index.js`: The entry point for the application.


## Reference dependencies docs
- [React Bootstrap](https://react-bootstrap.github.io/) <br>
- [React Icons](https://react-icons.github.io/react-icons/) <br/>


## Available Scripts
In this project directory you can run: <br/>
```
npm-start
```
This runs in development mode. Open [Local server](https://localhost:300) to view it in the browser. <br/>
```
npm test
```
Launches the test runner in the interactive watch mode <br/>
```
npm run build
```
Builds the app for production to `build` folder. <br/>


## Conclusion
This README file provides developers with a comprehensive guide to the GDSC Kabarak University Comrade Marketplace project's React frontend. It outlines the project's specifications, requirements, setup instructions, and information about how to contribute to the project. <br/>

By providing this information, developers can quickly understand the project's purpose, how it works, and what they need to do to get started. Additionally, the document outlines the project's development process, which will help contributors work more efficiently and contribute to the project's success. <br/>

HAVE FUN BUILDING AND LEARNING TOGETHER
