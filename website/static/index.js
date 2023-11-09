async function deleteNote(noteId){
    await fetch('/delete-note',  {
        method: 'POST',
         body: JSON.stringify({'noteId': noteId})
    })
    window.location.href = '/'
}

console.log("Hello")