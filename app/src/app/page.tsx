"use client"
import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Navbar, Nav, Container } from 'react-bootstrap';
import Loading from './loading';
import "./globals.css";
import { apiUploadSyllabus } from './api/apit';
import NavBar from './components/navbar';

export default function Home() {

    const [loading, setLoading] = useState<boolean>(false);
    const [showDownload, setShowDownlaod] = useState<boolean>(false);
    const [blobData, setBlobData] = useState<Blob | null>(null);

    const handleDownloadClick = () => {
        if (blobData) {
            const url = window.URL.createObjectURL(blobData);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'output.ics';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        }
    };

    const onDrop = useCallback((acceptedFiles : any) => {
        acceptedFiles.forEach((file: File) => {
            setLoading(true);
            if (file.type === 'application/pdf') {
                apiUploadSyllabus(file)
                    .then((data) => {
                        setLoading(false);
                        if (data) {
                            setBlobData(data);
                            setShowDownlaod(true);
                        }
                    })
            } else {
                console.log(`Invalid file type: ${file.name}`);
            }
        });
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

    return (
        <> 
            <NavBar></NavBar> 
            <Container className="d-flex flex-column align-items-center justify-content-center p-4">
                <div className="title">
                    &#128197; GPT-Calendar Generator
                </div> 
                <div className="sub-title">
                    Drop in a PDF syllabus to extract dates for Midterms, Quizes, Assignments and More!
                    Generate an ICS File that can be imported into any calendar.
                </div> 
                <div 
                    className="drop-container"
                    {...getRootProps()}
                    style={{
                        cursor: 'pointer',
                        border: '2px dashed #ccc',
                        borderRadius: '10px',
                        padding: '20px',
                        textAlign: 'center',
                        width: '60%',
                        transition: 'border .3s ease-in-out',
                        ...(isDragActive ? { border: '2px dashed #007BFF' } : showDownload ? { border: '2px dashed #007BFF' } : {}),
                    }}
                >
                    <input {...getInputProps()} />
                    {
                        isDragActive ?
                        <p style={{ color: '#007BFF', fontSize: '16px' }}>Drop the PDF here ...</p> :
                        showDownload? 
                        <p style={{ color: '#333', fontSize: '16px' }}> ICS file generation complete </p> :
                        <p style={{ color: '#333', fontSize: '16px' }}>Drag and drop a PDF here, or click to select a PDF</p> 
                    }
                </div>
                <div className="buttons-container">
                    <div className="download-button"
                        style={{ marginTop: '20px'}} 
                    >
                        { showDownload ? <button onClick={handleDownloadClick} type="button" className="btn btn-outline-primary">Download ICS file</button> : <></>}
                    </div>  
                </div>

                { loading ? <Loading></Loading> : <></> }
            </Container>
        </>
    );
}