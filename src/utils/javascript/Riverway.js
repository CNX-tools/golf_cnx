// Find the <mat-select> element and click on it to open the dropdown
const matSelect = document.querySelector('mat-select[name="course"]');
matSelect.click();

// Find the option you want to select and click on it
const optionToSelect = document.querySelector("#mat-option-4 > span");
optionToSelect.click();

// Find and click the apply filter button
const applyFilterButton = document.querySelector(
  "#mat-select-2-panel > app-search-mat-option-select-all > div > div.done-button > button > span.mat-button-wrapper"
);
applyFilterButton.click();
