function deleteQuestion(questionId) {
    fetch('/delete_question', {
        method: 'POST',
        body: JSON.stringify({ questionID: questionId})
    }).then((_res) => {
        window.location.href = "/add_card";
    })
}