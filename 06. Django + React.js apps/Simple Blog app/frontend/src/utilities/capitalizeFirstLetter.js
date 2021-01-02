const util = (word) => {
    
    const result = (word.length > 1) ? (word.charAt(0).toUpperCase() + word.slice(1)) : word.toUpperCase()
    return result
}

export default util