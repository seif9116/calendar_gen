import React, { useState } from 'react';
import { Navbar, Nav, Container } from 'react-bootstrap';
 

const NavBar = () => {

    return (
        <div>
            <Navbar bg="light" expand="lg">
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav" className="justify-content-center">
                    <Nav className="mr-auto">
                        <Nav.Link href="/" className="mx-4">Generate</Nav.Link>
                        <Nav.Link href="/about" className="mx-4">About</Nav.Link>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
        </div>
    );
}

export default NavBar;