async function deleteWord(wordId) {
    console.log(wordId)
    await fetch('/delete-word', {
        method: 'POST',
        body: JSON.stringify({'wordId': wordId})
    })
    window.location.href = '/trash'
}

async function remove(wordId) {
    console.log(wordId)
    await fetch('/remove', {
        method: 'POST',
        body: JSON.stringify({'wordId': wordId})
    })
    window.location.href = '/dictionary'
}

async function restore(wordId) {
    console.log(wordId)
    await fetch('/trash', {
        method: 'POST',
        body: JSON.stringify({'wordId': wordId})
    })
    window.location.href = '/trash'
}


console.log("Hello")