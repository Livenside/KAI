const topics = document.querySelectorAll('[data-topic]')

topics.forEach(topicEl => {
    topicEl.onclick = () => {
        const topic = topicEl.dataset.topic; // Получаем topic напрямую из атрибута
        const results = document.querySelector(`[data-topic-results="${topic}"]`)

        if (!results) return; // Проверяем, существует ли results

        topicEl.classList.toggle('active')
        results.classList.toggle('shown')
    }
})

document.getElementById('cb2').addEventListener('change', function() {
	var resultsContents = document.getElementById('resultscontents');
	var resultsContents2 = document.getElementById('resultscontents2');

	// Если чекбокс включен, скрываем resultscontents и показываем resultscontents2
	if (this.checked) {
		resultsContents.style.display = 'none';
		resultsContents2.style.display = 'block';
	} else {
		resultsContents.style.display = 'block';
		resultsContents2.style.display = 'none';
	}
});