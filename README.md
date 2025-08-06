# QTechy Assignment

## Objective

The goal of this task is to help you build a dynamic user interface using React, Tailwind CSS, and Cloudinary. You will develop three core UI components and a dashboard interface to dynamically update their content.

## Requirements

Technology Stack:

-   React (using Vite or Create React App)
-   Tailwind CSS
-   Cloudinary (for image upload functionality)

## Component Responsibilities

1. Header

-   Display a title.
-   Display an image (uploaded via Cloudinary).
-   Use Tailwind CSS for layout and design.

2. Navbar

-   Display three navigation links.
-   Each link should be editable via the dashboard (text + URL).
-   Align links horizontally using Tailwind.

3. Footer

-   Display contact information:
-   Email
-   Address
-   Phone number
-   All fields should be editable from the dashboard.

## Dashboard.jsx Features

Create a dashboard interface to edit/update content dynamically without page refresh.

1. Header:

-   Text input for title
-   Image upload input (Cloudinary integration)

2. Navbar:

-   Three input fields for link labels
-   Three input fields for link URLs

3. Footer:

-   Input for email
-   Input for phone number
-   Input for address Cloudinary Integration

You are required to integrate Cloudinary for image upload in the Header section.

## Steps to Set Up

1. Create a Cloudinary account and go to Upload Settings.
2. Create an unsigned upload preset.
3. Upload image from the dashboard and receive a URL.
4. Use the URL to dynamically display the image in the Header.

## Backend Work

-   Set up a Node.js + Express server
-   Create an endpoint to receive and store form data (optional for persistence)
-   Optional: Use MongoDB to store header, navbar, and footer data
-   Secure Cloudinary API keys using environment variables
-   Create a simple API endpoint `/api/components` for saving and fetching dynamic content
-   Ensure CORS is enabled to allow frontend requests Bonus (Optional)
-   Preview the image before uploading it.
-   Store form data in localStorage to retain changes after refresh.
-   Use React Context or Redux to manage state globally instead of prop drilling.
