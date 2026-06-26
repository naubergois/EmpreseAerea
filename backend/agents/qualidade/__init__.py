"""Agente de Qualidade — integra o SkyAgent ao SonarQube.

Consome as análises do SonarQube (issues, métricas, quality gate e security
hotspots), transforma os achados em um plano de melhorias priorizado e o
expõe via API REST para os demais agentes / frontend.
"""
