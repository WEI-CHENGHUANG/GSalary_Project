// setup
const data = {
  //labels: [The data will come from drop-down list values]
  datasets: [
    {
      label: "The number of Job Posts",
      //data: [here will be the number of jot posts by languages or db],
      backgroundColor: [
        "rgba(255, 26, 104, 0.2)",
        "rgba(54, 162, 235, 0.2)",
        "rgba(255, 206, 86, 0.2)",
        "rgba(75, 192, 192, 0.2)",
        "rgba(153, 102, 255, 0.2)",
        "rgba(255, 159, 64, 0.2)",
        "rgba(0, 0, 0, 0.2)",
      ],
      borderColor: [
        "rgba(255, 26, 104, 1)",
        "rgba(54, 162, 235, 1)",
        "rgba(255, 206, 86, 1)",
        "rgba(75, 192, 192, 1)",
        "rgba(153, 102, 255, 1)",
        "rgba(255, 159, 64, 1)",
        "rgba(0, 0, 0, 1)",
      ],
      borderWidth: 1,
    },
  ],
};
// config
const config = {
  type: "bar",
  data,
  options: { scales: { y: { beginAtZero: true } } },
};
// render init block
const myChart = new Chart(document.getElementById("myChart"), config);
function updateChart(stateName, userselected) {
  async function fetchData() {
    const urlLangs = "/api/languages";
    const response = await fetch(urlLangs);

    const langsData = await response.json();
    return langsData;
  }

  fetchData().then((langsData) => {
    let langsCounts = langsData.all_langs_counts_by_state[stateName];
    let dbCounts = langsData.all_dbs_counts_by_state[stateName];
    let langsDbs = [];
    let counts = [];

    langsCounts.forEach((val) => {
      lan = Object.keys(val)[0];
      if (userselected.includes(lan)) {
        langsDbs.push(lan);
        counts.push(Object.values(val)[0]);
      }
    });
    dbCounts.forEach((val) => {
      db = Object.keys(val)[0];
      if (userselected.includes(db)) {
        langsDbs.push(db);
        counts.push(Object.values(val)[0]);
      }
    });
    myChart.config.data.labels = langsDbs;
    myChart.config.data.datasets[0].data = counts;
    myChart.update();
  });
}
// ===========drop-down List==================================

function createPGDBList(urllangs, PL_or_DB, stateName, listOrlist1) {
  fetch(urllangs)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      let langsDbByState = data[PL_or_DB][stateName];
      if (PL_or_DB === "all_dbs_counts_by_state") {
        for (let i = 0; i < langsDbByState.length; i++) {
          let name = Object.keys(langsDbByState[i])[0];
          // The newNum is to distinguish the input tag id nmber in order to avoid selected issue.
          newNum = i + 100;
          createLabel(name, newNum, listOrlist1, name);
        }
      } else {
        for (let i = 0; i < langsDbByState.length; i++) {
          let name = Object.keys(langsDbByState[i])[0];
          //console.log(name)
          createLabel(name, i, listOrlist1, name);
        }
      }
      // The code below is to limit the max selection from PL list
      let max = 8;
      let Checkboxes = document.querySelectorAll(".single-checkbox");

      for (let i = 0; i < Checkboxes.length; i++)
        Checkboxes[i].onclick = selectiveCheck;
      function selectiveCheck(event) {
        var checkedChecks = document.querySelectorAll(
          ".single-checkbox:checked"
        );
        if (checkedChecks.length >= max + 1) return false;
      }
    })
    .catch((error) => {
      console.log(
        error,
        "Something went wrong when fetching data via API, Check JS function : createPGDBList(urllangs, PL_or_DB, stateName, listOrlist1)"
      );
    });
}

function createLabel(name1, count, listOrlist1, value) {
  count += 1;
  let list = document.querySelector(`.${listOrlist1}`);
  let label = document.createElement("label");
  label.className = "task";
  label.setAttribute("for", `task${count}`);
  let input = document.createElement("input");
  input.id = `task${count}`;
  input.className = "single-checkbox";
  input.setAttribute("type", "checkbox");
  input.setAttribute("name", "subject");
  input.setAttribute("value", value);
  label.append(input);
  label.append(name1);
  list.append(label);
}
// this is for little triangle icon (PL).
document.querySelector(".select-field").addEventListener("click", () => {
  document.querySelector(".list").classList.toggle("show");
  document.querySelector(".down-arrow").classList.toggle("rotate180");
});

// this is for little triangle icon (DB).
document.querySelector(".select-field1").addEventListener("click", () => {
  document.querySelector(".list1").classList.toggle("show");
  document.querySelector(".down-arrow").classList.toggle("rotate180");
});
// ==========================================================
//* stateName => this is from state.js because two JS files are connected to one file, state.html.
let urllangs = "/api/languages";
let PL = "all_langs_counts_by_state";
let DB = "all_dbs_counts_by_state";
createPGDBList(urllangs, PL, stateName, "list"); // className = ".list" => Programming Languages
createPGDBList(urllangs, DB, stateName, "list1"); // className = ".list1" => Database

// This is waiting for user's input from drop-down list.
const bt = document.querySelector("#renderdata");
bt.addEventListener("click", (event) => {
  let checkedboxes = document.querySelectorAll('input[name="subject"]:checked');
  let output = [];
  checkedboxes.forEach((checkbox) => {
    output.push(checkbox.value);
  });
  updateChart(stateName, output);
});
