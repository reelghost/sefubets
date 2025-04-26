// Get all elements with a title attribute
const overDiv = document.querySelector("div#main").querySelector("header");
const elementsWithTitle = overDiv.querySelectorAll('span.copyable-text');

// Extract and split raw title text from each, flattening by comma
const titles = Array.from(elementsWithTitle)
  .flatMap(el => el.textContent.split(',').map(s => s.trim()))
  .filter(Boolean);

// Remove duplicates
const uniqueTitles = [...new Set(titles)];

// Log what we're saving
console.log('📝 Titles to save:', uniqueTitles);

// Build the CSV content
const csvContent = 'data:text/csv;charset=utf-8,' + uniqueTitles.join('\n');

// Trigger download
const encodedUri = encodeURI(csvContent);
const link = document.createElement('a');
link.setAttribute('href', encodedUri);
link.setAttribute('download', 'contacts.csv');
document.body.appendChild(link);
link.click();
document.body.removeChild(link);
