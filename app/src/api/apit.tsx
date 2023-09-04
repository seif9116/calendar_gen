export const apiUploadSyllabus = async (file: File) => {
    const formData = new FormData();
    formData.append('syllabus', file);

    const PORT_ENV = process.env.PORT;
    const PORT = PORT_ENV === undefined ? 5000 : PORT_ENV;
    const APP_URI = process.env.DEPLOY_MODE === 'DEV' 
        ? 'http://localhost:5000' 
        : 'https://calendar-gen-5b245af668f0.herokuapp.com';

    console.log("environment:", PORT, APP_URI);
    try {
        // const response = await fetch(`http://0,0,0,0:${PORT}/api/syllabus`, {
        const response = await fetch(`${APP_URI}:${PORT}/api/syllabus`, {
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