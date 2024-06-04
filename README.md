
# Wallet and Transaction API

This project is a REST API server built using Django and Django REST Framework with JSON:API specification. It provides endpoints for managing wallets and transactions with features like pagination, sorting, and filtering.

## Models

### Wallet
- `id`: Primary key
- `label`: String field
- `balance`: Decimal field (18 digits of precision)

### Transaction
- `id`: Primary key
- `wallet_id`: Foreign key to Wallet
- `txid`: Unique string field
- `amount`: Decimal field (18 digits of precision)

## Features
- Pagination
- Sorting
- Filtering

## Endpoints

### Wallet Endpoints
- `GET /wallets/`: List all wallets
- `POST /wallets/`: Create a new wallet
- `GET /wallets/{id}/`: Retrieve a wallet by ID
- `PATCH /wallets/{id}/`: Update a wallet by ID
- `DELETE /wallets/{id}/`: Delete a wallet by ID

### Transaction Endpoints
- `GET /transactions/`: List all transactions
- `POST /transactions/`: Create a new transaction
- `GET /transactions/{id}/`: Retrieve a transaction by ID
- `DELETE /transactions/{id}/`: Delete a transaction by ID

## Quick Start Guide

### Prerequisites
- Docker
- Docker Compose

### Setup

1. Clone the repository:

```bash
git clone https://github.com/kirill-ilichev/WalletAndTransactions.git
cd WalletAndTransactions
```

2. Set up environment variables:

Create a `.env` file in the root directory and add the following:

```
DATABASE_URL=mysql://yourdbuser:yourdbpassword@localhost:3306/yourdbname
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost, 127.0.0.1
```

3. Run Docker Compose:

```bash
docker-compose up --build
```

4. Apply migrations:

```bash
docker-compose exec web ./manage.py migrate
```

5. Access the API:

The API will be available at `http://localhost:8000`.

## Running Tests

To run tests, use the following command:

```bash
docker-compose exec web ./manage.py test
```

## Grant MySQL Privileges

Run the following commands to grant the necessary privileges:

1. Access the MySQL shell:

```bash
docker-compose exec db mysql -u root -p
```

2. In the MySQL shell, run:

```sql
GRANT ALL PRIVILEGES ON test_yourdbname.* TO 'yourdbuser'@'%';
FLUSH PRIVILEGES;
```

## Code Quality

This project uses `flake8` for linting and `black` for code formatting.

### Running Linter

```bash
docker-compose exec web flake8 .
```

### Running Formatter

```bash
docker-compose exec web black .
```
