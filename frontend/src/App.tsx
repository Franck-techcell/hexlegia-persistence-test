import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  CircularProgress,
  Alert,
  Grid,
  Card,
  CardContent,
} from '@mui/material';
import axios from 'axios';

// Types
interface HealthStatus {
  status: string;
  app?: string;
  version?: string;
  timestamp?: string;
  debug?: boolean;
}

const App: React.FC = () => {
  const [healthStatus, setHealthStatus] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHealthStatus = async () => {
      try {
        const response = await axios.get<HealthStatus>('/api/health');
        setHealthStatus(response.data);
      } catch (err) {
        setError('Impossible de se connecter au backend');
        console.error('Error fetching health status:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchHealthStatus();
  }, []);

  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h2" component="h1" gutterBottom>
        HexLegIA
      </Typography>

      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Socle Technique V1
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12} md={6} lg={4}>
          <Card>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom>
                État du Système
              </Typography>
              
              {healthStatus ? (
                <>
                  <Alert
                    severity={healthStatus.status === 'ok' ? 'success' : 'warning'}
                    sx={{ mb: 2 }}
                  >
                    {healthStatus.status === 'ok' ? '✅ Système opérationnel' : '⚠️ Problème détecté'}
                  </Alert>
                  
                  <Typography variant="body2" color="text.secondary">
                    <strong>Application:</strong> {healthStatus.app || 'HexLegIA'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    <strong>Version:</strong> {healthStatus.version || '1.0.0'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    <strong>Mode:</strong> {healthStatus.debug ? 'Développement' : 'Production'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    <strong>Timestamp:</strong> {healthStatus.timestamp || 'N/A'}
                  </Typography>
                </>
              ) : (
                <Alert severity="warning">Aucune donnée de santé disponible</Alert>
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6} lg={4}>
          <Card>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom>
                État de l'API
              </Typography>
              
              {healthStatus?.status === 'ok' ? (
                <Alert severity="success">API Backend accessible</Alert>
              ) : (
                <Alert severity="error">API Backend inaccessible</Alert>
              )}
              
              <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                L'API FastAPI est configurée avec l'endpoint <code>/health</code> pour vérifier
                l'état du backend.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6} lg={4}>
          <Card>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom>
                Version du Socle
              </Typography>
              
              <Typography variant="h6" gutterBottom>
                HexLegIA V1
              </Typography>
              
              <Typography variant="body2" color="text.secondary">
                <strong>Frontend:</strong> React 18 + TypeScript
              </Typography>
              <Typography variant="body2" color="text.secondary">
                <strong>Backend:</strong> FastAPI + Python 3.11
              </Typography>
              <Typography variant="body2" color="text.secondary">
                <strong>Base de données:</strong> PostgreSQL 15
              </Typography>
              <Typography variant="body2" color="text.secondary">
                <strong>Recherche vectorielle:</strong> Qdrant
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Box sx={{ mt: 4, p: 2, bgcolor: 'background.paper', borderRadius: 1 }}>
        <Typography variant="body2" color="text.secondary">
          © {new Date().getFullYear()} Franck-techcell. Tous droits réservés.
        </Typography>
      </Box>
    </Box>
  );
};

export default App;
