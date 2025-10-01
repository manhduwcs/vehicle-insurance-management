document.addEventListener("DOMContentLoaded", function () {
 const deleteBtn = document.getElementById("deleteBtn");
 const deleteConfirm = document.getElementById("deleteConfirm");
 const overlay = document.getElementById("overlay");
 const cancelBtn = document.getElementById("cancelDelete");

 function showModal() {
  deleteConfirm.style.display = "block";
  overlay.style.display = "block";
 }

 function hideModal() {
  deleteConfirm.style.display = "none";
  overlay.style.display = "none";
 }

 deleteBtn.addEventListener("click", showModal);
 cancelBtn.addEventListener("click", hideModal);
 overlay.addEventListener("click", hideModal);
});