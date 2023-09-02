export const apiUploadSyllabus = async (file: File) => {
    const formData = new FormData();
    formData.append('syllabus', file);

    try {
        const response = await fetch('http://localhost:5000/api/syllabus', {
            method: 'POST',
            body: formData,
        }); 
        if (response.ok) { 
            const blob = await response.blob();
            return blob; 
        } else {
            console.log('Upload failed', response);
            return null;
        } 
    } catch (error) {
        console.error('There was a problem uploading the file', error);
    }
};