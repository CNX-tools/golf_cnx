const dayUnitElements = document.querySelectorAll(".day-unit");

const isActiveElements = Array.from(dayUnitElements).filter((element) => {
  return (
    element.querySelector(".day-background-upper.is-visible") &&
    !element.querySelector(".day-background-upper.is-disabled")
  );
});

const result = isActiveElements.map((element) => {
  const cssSelector = `.day-unit:nth-child(${Array.from(element.parentElement.children).indexOf(element) + 1})`;
  const textContent = element.querySelector(".day-background-upper").textContent;
  return [cssSelector, textContent];
});

return result;
