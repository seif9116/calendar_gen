import { useRouter } from 'next/navigation'; 
import React, { useState } from 'react';
import { Navbar, Nav, Container } from 'react-bootstrap';
import "../app/globals.css";
import NavBar from '@/app/components/navbar';

import 'bootstrap/dist/css/bootstrap.min.css';
import '@/app/globals.css';

const AboutPage: React.FC = () => {
    return (
        <div>
            <NavBar></NavBar> 
             <Container className="d-flex flex-column align-items-center justify-content-center p-4">
                <div className="title">
                    &#128197; About
                </div> 
                <div className="about-section">

                    
                    Calendar-Gen was created by Seif and Justin...
                    <br></br><br></br> 
                    
                    It works by using OpenAI embeddings to... 
                    
                    <br></br><br></br> 
                    The code can be found <a href="">here</a>. The project was written in a few days, so there 
                    are many poor code practices (sorry cmput 301 &#128517; .) The purpose of publishing is 
                    soley to provide transparency for those curious about how we handle user data.
        
                </div> 
               
            </Container>

        </div>
    );
};

export default AboutPage;
