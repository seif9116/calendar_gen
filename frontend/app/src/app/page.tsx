"use client"
import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Navbar, Nav, Container } from 'react-bootstrap';
import Loading from './loading';
import "./globals.css";

export const apiUploadSyllabus = async (file: File) => {
    const formData = new FormData();
    formData.append('syllabus', file);

    try {
        const response = await fetch('http://localhost:5000/api/syllabus', {
            method: 'POST',
            body: formData,
        });

        // Inside apiUploadSyllabus function
        if (response.ok) { 
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'output.ics';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        } else {
            console.log('Upload failed', response);
        } 
    } catch (error) {
        console.error('There was a problem uploading the file', error);
    }
};

export default function Home() {
    const [loading, setLoading] = useState<boolean>(true);
    
    const onDrop = useCallback((acceptedFiles : any) => {
        acceptedFiles.forEach((file: File) => {
            if (file.type === 'application/pdf') {
                console.log(`Received PDF: ${file.name}`);
                // Handle the PDF file
                console.log(file);
                setLoading(true);
                const res = apiUploadSyllabus(file);
                console.log(res);

                setLoading(false);

            } else {
                console.log(`Invalid file type: ${file.name}`);
            }
        });
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

    return (
        <> 
            <Navbar bg="light" expand="lg">
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav" className="justify-content-center">
                    <Nav className="mr-auto">
                        <Nav.Link href="/" className="mx-4">Generate</Nav.Link>
                        <Nav.Link href="/about" className="mx-4">About</Nav.Link>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
            

            <Container className="d-flex flex-column align-items-center justify-content-center p-4">
                <div className="title">
                    &#128197; GPT-Calendar Generator
                </div> 
                
                <div 
                    className="drop-container"
                    {...getRootProps()}
                    style={{
                        border: '2px dashed #ccc',
                        borderRadius: '10px',
                        padding: '20px',
                        textAlign: 'center',
                        width: '100%',
                        transition: 'border .3s ease-in-out',
                        ...(isDragActive ? { border: '2px dashed #007BFF' } : {}),
                    }}
                >
                    <input {...getInputProps()} />
                    {
                        isDragActive ?
                        <p style={{ color: '#007BFF', fontSize: '16px' }}>Drop the PDF here ...</p> :
                        <p style={{ color: '#333', fontSize: '16px' }}>Drag 'n' drop a PDF here, or click to select a PDF</p>
                    }
                </div>
                { loading ? <Loading></Loading> : <></>}
            </Container>
        </>
    );
}