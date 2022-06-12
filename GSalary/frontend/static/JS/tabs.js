function createTableForLangDb(
  templateTag,
  containerTag,
  numberTag,
  nameTag,
  countsTag,
  count,
  pgdbname,
  jobCounts
) {
  const allpgdbTemplate = document.querySelector(templateTag);
  const allaupgContainer = document.querySelector(containerTag);
  const eachtable = allpgdbTemplate.content.cloneNode(true).children[0];
  const allpgdbNumber = eachtable.querySelector(numberTag);
  const allpgdbName = eachtable.querySelector(nameTag);
  const allpgdbCounts = eachtable.querySelector(countsTag);
  allpgdbNumber.textContent = count;
  allpgdbName.textContent = pgdbname;
  allpgdbCounts.textContent = jobCounts;
  allaupgContainer.append(eachtable);
}

function insertdataTo4Tables(url) {
  fetch(url)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      // ===========table 1========
      let templateTag1 = "[allpgdb-template1]";
      let containerTag1 = "[allaupg-container1]";
      let numberTag1 = "[allpgdb-number1]";
      let nameTag1 = "[allpgdb-name1]";
      let countsTag1 = "[allpgdb-counts1]";
      let numberCount1 = 0;
      data["all_langs_counts"].forEach((data) => {
        numberCount1 += 1;
        let pgName = Object.keys(data);
        let pgCount = data[Object.keys(data)];
        createTableForLangDb(
          templateTag1,
          containerTag1,
          numberTag1,
          nameTag1,
          countsTag1,
          numberCount1,
          pgName,
          pgCount
        );
      });
      // ===========table 2========
      let templateTag2 = "[allpgdb-template2]";
      let containerTag2 = "[allaupg-container2]";
      let numberTag2 = "[allpgdb-number2]";
      let nameTag2 = "[allpgdb-name2]";
      let countsTag2 = "[allpgdb-counts2]";
      let numberCount2 = 0;
      data["all_dbs_counts"].forEach((data) => {
        numberCount2 += 1;
        let dbName = Object.keys(data);
        let dbCount = data[Object.keys(data)];
        createTableForLangDb(
          templateTag2,
          containerTag2,
          numberTag2,
          nameTag2,
          countsTag2,
          numberCount2,
          dbName,
          dbCount
        );
      });
      // ===========table 3========
      let templateTag3 = "[allpgdb-template3]";
      let containerTag3 = "[allaupg-container3]";
      let numberTag3 = "[allpgdb-number3]";
      let nameTag3 = "[allpgdb-name3]";
      let countsTag3 = "[allpgdb-counts3]";

      for (let i = 0; i < data["top_five_pg_by_state"].length; i++) {
        let pgStateName = Object.keys(data["top_five_pg_by_state"][i]);
        let pgStateCount = data["top_five_pg_by_state"][i][pgStateName];
        pgStateCount.forEach((data) => {
          let pgNameState = Object.keys(data);
          let pgCountState = data[pgNameState];
          createTableForLangDb(
            templateTag3,
            containerTag3,
            numberTag3,
            nameTag3,
            countsTag3,
            pgStateName,
            pgNameState,
            pgCountState
          );
        });
      }
      // ===========table 4========
      let templateTag4 = "[allpgdb-template4]";
      let containerTag4 = "[allaupg-container4]";
      let numberTag4 = "[allpgdb-number4]";
      let nameTag4 = "[allpgdb-name4]";
      let countsTag4 = "[allpgdb-counts4]";

      for (let i = 0; i < data["top_five_db_by_state"].length; i++) {
        let dbStateName = Object.keys(data["top_five_db_by_state"][i]);
        let dbStateCount = data["top_five_db_by_state"][i][dbStateName];
        dbStateCount.forEach((data) => {
          let dbNameState = Object.keys(data);
          let dbCountState = data[dbNameState];
          createTableForLangDb(
            templateTag4,
            containerTag4,
            numberTag4,
            nameTag4,
            countsTag4,
            dbStateName,
            dbNameState,
            dbCountState
          );
        });
      }

      const JobPostsTitle = document.querySelector("#JobPostsTitle");
      JobPostsTitle.style.display = "block";

      const pillsTabContent = document.querySelector("#pills-tabContent");
      pillsTabContent.style.display = "block";

      const loader4 = document.querySelector(".loader4");
      loader4.style.display = "none";
    })
    .catch((error) => {
      console.log(
        error,
        "Something went wrong when fetching data via API, Check JS function : userQueryCompany()"
      );
    });
}
const urlLangs = "/api/languages";
insertdataTo4Tables(urlLangs);
