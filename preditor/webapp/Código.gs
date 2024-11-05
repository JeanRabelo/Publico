function doGet() {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('Word Association Finder');
}

