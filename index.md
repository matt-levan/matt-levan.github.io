---
layout: home
title: Home
permalink: /
nav_order: 1
---

# IBM Storage Technical Library

Welcome to the IBM Storage technical documentation library. Select a guide below to get started.

<div class="doc-cards">

  <a href="/fusion-demo-guide/" class="doc-card">
    <h2>IBM Fusion Demo Guide</h2>
    <p>Hands-on demo guide for platform modernization with IBM Fusion. Covers installation, storage, backup, and restore on OpenShift.</p>
    <span class="doc-card-version">v2.13.1</span>
  </a>

  <a href="/backup-restore-guide/" class="doc-card">
    <h2>Fusion Backup &amp; Restore Lab Guide</h2>
    <p>Hands-on labs for IBM Fusion Backup &amp; Restore — policies, recipes, application-consistent backups, and hub/spoke restore.</p>
    <span class="doc-card-version">v2.12.0.0</span>
  </a>

  <a href="#" class="doc-card doc-card-coming-soon">
    <h2>Fusion Regional Disaster Recovery Guide</h2>
    <p>Configure and test regional disaster recovery with IBM Fusion hub-and-spoke architecture.</p>
    <span class="doc-card-badge">Coming soon</span>
  </a>

</div>

<style>
.doc-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.25rem;
  margin-top: 2rem;
}
.doc-card {
  display: block;
  padding: 1.25rem 1.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  text-decoration: none;
  color: inherit;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.doc-card:hover {
  border-color: #2c84fa;
  box-shadow: 0 2px 8px rgba(44,132,250,0.12);
  text-decoration: none;
}
.doc-card h2 {
  margin: 0 0 0.5rem;
  font-size: 1.05rem;
  color: #2c84fa;
  border: none;
}
.doc-card p {
  margin: 0 0 0.75rem;
  font-size: 0.9rem;
  color: #57606a;
  line-height: 1.5;
}
.doc-card-version {
  font-size: 0.78rem;
  color: #57606a;
  background: #f0f4ff;
  padding: 0.15em 0.5em;
  border-radius: 3px;
}
.doc-card-coming-soon {
  opacity: 0.6;
  cursor: default;
  pointer-events: none;
}
.doc-card-badge {
  font-size: 0.78rem;
  color: #ffffff;
  background: #57606a;
  padding: 0.15em 0.5em;
  border-radius: 3px;
}
</style>
