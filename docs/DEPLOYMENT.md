# Deployment Guide

## Overview

NetworkCellularMap v2.0 can be deployed using Docker Compose (recommended for development/testing) or Kubernetes (recommended for production).

## Docker Compose Deployment

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/ncsound919/Cellular-Map.git
cd Cellular-Map
```

2. **Configure environment**
```bash
cd backend
cp .env.example .env
# Edit .env with your configuration
```

3. **Start services**
```bash
docker-compose up -d
```

4. **Verify deployment**
```bash
docker-compose ps
```

5. **Access services**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Neo4j Browser: http://localhost:7474

### Stopping Services
```bash
docker-compose down
```

### Viewing Logs
```bash
docker-compose logs -f [service_name]
```

## Kubernetes Deployment

### Prerequisites
- Kubernetes cluster (1.25+)
- kubectl configured
- Sufficient cluster resources

### Steps

1. **Build and push Docker images**
```bash
# Backend
cd backend
docker build -t your-registry/networkology-backend:2.0 .
docker push your-registry/networkology-backend:2.0

# Frontend
cd ../frontend
docker build -t your-registry/networkology-frontend:2.0 .
docker push your-registry/networkology-frontend:2.0
```

2. **Update image references**
Edit `kubernetes/deployment.yaml` to use your registry images.

3. **Deploy to Kubernetes**
```bash
kubectl apply -f kubernetes/deployment.yaml
```

4. **Verify deployment**
```bash
kubectl get pods -n networkology
kubectl get services -n networkology
```

5. **Access services**
```bash
# Port forward frontend
kubectl port-forward -n networkology svc/frontend 3000:80

# Port forward backend
kubectl port-forward -n networkology svc/ai-scientist 8000:8000
```

### Scaling

The backend includes horizontal pod autoscaling:
```bash
kubectl get hpa -n networkology
```

To manually scale:
```bash
kubectl scale deployment backend -n networkology --replicas=5
```

### Monitoring

Check logs:
```bash
kubectl logs -n networkology -l app=backend -f
```

### Updating

To update a deployment:
```bash
kubectl set image deployment/backend -n networkology backend=your-registry/networkology-backend:2.1
```

## Production Considerations

### Security
1. **Enable authentication** - Add OAuth2 or JWT to API endpoints
2. **Use secrets** - Store sensitive data in Kubernetes secrets or environment variables
3. **Network policies** - Restrict traffic between pods
4. **TLS/SSL** - Enable HTTPS for frontend and API

### Performance
1. **Database tuning** - Configure Neo4j for your workload
2. **Caching** - Use Redis for frequently accessed data
3. **CDN** - Serve frontend static assets via CDN
4. **Load balancing** - Use ingress controller for proper load distribution

### Monitoring
1. **Prometheus** - Collect metrics
2. **Grafana** - Visualize metrics
3. **ELK Stack** - Centralized logging
4. **Health checks** - Configure liveness and readiness probes

### Backup
1. **Neo4j backups** - Regular database backups
2. **Volume snapshots** - Snapshot persistent volumes
3. **Configuration backups** - Version control all configs

## Troubleshooting

### Backend won't start
```bash
# Check logs
docker-compose logs backend
# or
kubectl logs -n networkology -l app=backend

# Common issues:
# - Database connection failed: Check NEO4J_URI
# - Missing dependencies: Rebuild Docker image
```

### Frontend won't connect to backend
```bash
# Check environment variable
echo $NEXT_PUBLIC_API_URL

# Update docker-compose.yml or deployment.yaml
```

### Neo4j connection issues
```bash
# Test connection
docker-compose exec backend python -c "from app.db.neo4j import db_connection; db_connection.connect()"
```

### Out of memory
```bash
# Increase container limits in docker-compose.yml or deployment.yaml
```

## Health Checks

### Backend health
```bash
curl http://localhost:8000/health
```

### Neo4j health
```bash
curl http://localhost:7474/
```

### Overall system health
```bash
curl http://localhost:8000/
```
