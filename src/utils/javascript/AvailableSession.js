var buttonsArr = document.querySelectorAll('button[class="btnStepper"]');

const result = Array.from(buttonsArr).map((element) => {
  const cssSelector = `button[class="btnStepper"]:nth-child(${
    Array.from(element.parentElement.children).indexOf(element) + 1
  })`;
  const textContent = element.textContent;
  return [cssSelector, textContent];
});

result;
