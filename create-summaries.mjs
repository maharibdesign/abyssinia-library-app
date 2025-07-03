// create-summaries.mjs
import fs from 'fs';
import path from 'path';

// --- Configuration ---
const dataFilePath = './detailed-summaries-data.json';
const outputDir = './src/content/summaries';
// -------------------

function main() {
  console.log('--- Starting Detailed Summary Creation Script ---');

  if (!fs.existsSync(outputDir)) {
    console.log(`Creating directory: ${outputDir}`);
    fs.mkdirSync(outputDir, { recursive: true });
  }

  let summaries;
  try {
    const jsonData = fs.readFileSync(dataFilePath, 'utf-8');
    summaries = JSON.parse(jsonData);
    console.log(`-> Loaded ${summaries.length} summaries from data file.`);
  } catch (error) {
    console.error(`🛑 ERROR: Could not read or parse ${dataFilePath}. Aborting.`, error);
    return;
  }

  let filesCreated = 0;
  summaries.forEach(summary => {
    const filePath = path.join(outputDir, `${summary.slug}.md`);
    
    // The content for the .md file is now just the 'content' field from the JSON
    const markdownFileContent = `---
title: "${summary.title}"
author: "${summary.author}"
category: "${summary.category}"
description: "${summary.description}"
pdfUrl: "${summary.pdfUrl}"
---
${summary.content}
`;

    try {
      fs.writeFileSync(filePath, markdownFileContent);
      console.log(`  -> Successfully created/updated: ${summary.slug}.md`);
      filesCreated++;
    } catch (error) {
      console.error(`🛑 ERROR writing file ${filePath}:`, error);
    }
  });

  console.log(`\n✅ Script finished. Total files created/updated: ${filesCreated}`);
}

main();