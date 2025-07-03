# AbyssiniaLibrary Book Summary Mini App

This is a minimalistic, fast, and responsive web application for reading book summaries. It's built with modern tools and is designed to be easily maintainable.

The live application is deployed on Vercel.

## Features

- **Blazing Fast:** Built with Astro for a super-fast static site experience.
- **Dynamic Content:** Summaries are written in Markdown and loaded automatically.
- **Interactive UI:**
  - Save your favorite summaries, remembered on your device.
  - Live search by title or author.
  - Filter summaries by category.
- **Pro Features:**
  - Reading progress bar on summary pages.
  - "Random Summary" button for discovery.
  - Web Share API integration (falls back to "copy link").
- **Responsive Design:** Works beautifully on desktop and mobile.

## Tech Stack

- **Framework:** [Astro](https://astro.build/)
- **UI Components:** [React](https://react.dev/) (for interactive elements)
- **State Management:** [Nanostores](https://github.com/nanostores/nanostores)
- **Styling:** Plain CSS with CSS Variables
- **Deployment:** [Vercel](https://vercel.com/)

## How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/abyssinia-library-app.git
    cd abyssinia-library-app
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Start the development server:**
    ```bash
    npm run dev
    ```
    The application will be available at `http://localhost:4321`.

## How to Add a New Book Summary

1.  Create a new Markdown file in the `src/content/summaries/` directory. The filename will become the URL slug (e.g., `new-book.md` becomes `/summaries/new-book`).
2.  Add the required frontmatter to the top of the file:
    ```markdown
    ---
    title: "New Book Title"
    author: "Book Author"
    category: "Category Name"
    description: "A short, one-sentence description of the book."
    ---
    
    Your full summary content, written in Markdown, goes here...
    ```
3.  That's it! The new summary will automatically appear on the homepage.