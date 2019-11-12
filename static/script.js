const testFunc = async () => {
  const resp = await fetch("http://localhost:5000/test", {
    "Content-Type": "application/json",
    method: "POST"
  });
  console.log("Raw response: ", resp);
  const json = await resp.json();
  console.log("JSON: ", json);
};

const testFunc_2 = async () => {
  const resp = await fetch("http://localhost:5000/test", {
    "Content-Type": "application/json",
    method: "POST",
    body: JSON.stringify({ username: "jsmith", password: "password2" })
  });
  console.log("Raw response: ", resp);
  const json = await resp.json();
  console.log("JSON: ", json);
};

window.addEventListener("load", testFunc);
document.querySelector(".wrapper").addEventListener("click", testFunc_2);
