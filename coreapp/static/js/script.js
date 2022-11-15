async function copyContent(email) {
    try {
      await navigator.clipboard.writeText(email);
      console.log('Content copied to clipboard');
    } catch (err) {
      console.error('Failed to copy: ', err);
    }
  }