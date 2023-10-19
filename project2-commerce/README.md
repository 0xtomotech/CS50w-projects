# Project Commerce: Auctions Web Application

- [App Demo on Youtube](https://youtu.be/vmBd0o46UgM)
- [Project Instructions](https://cs50.harvard.edu/web/2020/projects/2/commerce/)

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Configuration](#configuration)
   - [Settings](#settings)
   - [URLs](#urls)
   - [Forms](#forms)
   - [Models](#models)
4. [Installation & Setup](#installation--setup)
5. [Security](#security)
6. [Contribution & Development](#contribution--development)

## Introduction

This Django web application was created as part of Harvard 's CS50W course. Commerce is a Django-based web application designed to facilitate online auctions. Users can post auction listings, place bids, comment on listings, and add listings to a watchlist.

## Features

- **User Authentication**: Register, log in, and log out.
- **Auction Listings**: Create, bid, and comment on listings. Listings can be added to a personal watchlist.
- **Close Auction**: Listing creators can close the auction. The highest bid becomes the winning bid, marking the listing as sold to the highest bidder.
- **Won Auctions**: View listings won.
- **Admin Interface**: Integrated Django's built-in admin interface.

## Configuration

### Settings

#### Project Directories & Paths
- **BASE_DIR**: The base directory of the project.
- **STATIC_URL**: URL for static files.

#### Development & Production
- **DEBUG**: Debug mode is on. Set to `False` for production.
- **ALLOWED_HOSTS**: Update for production.

#### Installed Apps
- **Custom Apps**: `auctions`
- **Django Default Apps**: `admin`, `auth`, `contenttypes`, `sessions`, `messages`, `staticfiles`

#### Middleware
Includes SecurityMiddleware, SessionMiddleware, CommonMiddleware, and others.

#### Database
Uses SQLite. Database file path is within the base directory.

### URLs

Key patterns include `/admin/`, `/`, `/login`, `/logout`, `/register`, `/createlisting/`, and more.

### Forms

Django forms like **CreateListingForm**, **BidForm**, **CommentForm**, and **CategoryFilterForm** are used.

### Models

Includes **User**, **Category**, **Listing**, **Bid**, **Comment**, and **Watchlist**.

## Installation & Setup

1. Clone the repository.
2. Navigate to the project directory.
3. Install required packages.
4. Run migrations.
5. Start the server.

## Security

Update **SECRET_KEY** for production. Set **DEBUG** to `False` in production.

## Contribution & Development

1. Fork the repo.
2. Make changes.
3. Submit a pull request.
