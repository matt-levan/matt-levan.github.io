---
layout: default
title: Home
permalink: /
nav_order: 0
---

# IBM Storage Technical Library

Welcome to the IBM Storage technical documentation library. Select a guide below to get started.

<div class="doc-cards">

  <a href="/fusion-demo-guide/" class="doc-card">
    <div class="doc-card-body">
      <h2>IBM Fusion Demo Guide</h2>
      <p>Hands-on demo guide for platform modernization with IBM Fusion. Covers installation, storage, backup, and restore on OpenShift.</p>
    </div>
    <div class="doc-card-footer">
      <span class="doc-card-version">v2.13.1</span>
      <span class="doc-card-arrow">Open →</span>
    </div>
  </a>

  <a href="/backup-restore-guide/" class="doc-card">
    <div class="doc-card-body">
      <h2>Fusion Backup &amp; Restore Lab Guide</h2>
      <p>Hands-on labs for IBM Fusion Backup &amp; Restore — policies, recipes, application-consistent backups, and hub/spoke restore.</p>
    </div>
    <div class="doc-card-footer">
      <span class="doc-card-version">v2.12.0.0</span>
      <span class="doc-card-arrow">Open →</span>
    </div>
  </a>

  <a href="/ocpv-fusion-lab/" class="doc-card">
    <div class="doc-card-body">
      <h2>OCP Virtualization with IBM Fusion Lab</h2>
      <p>Hands-on lab for modernizing virtualization with Red Hat OpenShift Virtualization and IBM Fusion — VM lifecycle, live migration, storage, and backup.</p>
    </div>
    <div class="doc-card-footer">
      <span class="doc-card-version">v4.20 / Fusion 2.12</span>
      <span class="doc-card-arrow">Open →</span>
    </div>
  </a>

  <a href="/hcp-lab-guide/" class="doc-card">
    <div class="doc-card-body">
      <h2>IBM Fusion HCP Lab Guide</h2>
      <p>Deploy IBM Fusion with OpenShift Hosted Control Planes — LVM storage, Fusion Data Foundation in Provider mode, MetalLB, multicluster engine, and hosted cluster creation.</p>
    </div>
    <div class="doc-card-footer">
      <span class="doc-card-version">v2.11.0.0</span>
      <span class="doc-card-arrow">Open →</span>
    </div>
  </a>

  <a href="/rdr-lab-guide/" class="doc-card">
    <div class="doc-card-body">
      <h2>IBM Fusion RDR Lab Guide</h2>
      <p>Implement and test Regional Disaster Recovery with IBM Fusion — two OpenShift clusters, Fusion Data Foundation, RHACM, Submariner, and OpenShift DR failover/relocate exercises.</p>
    </div>
    <div class="doc-card-footer">
      <span class="doc-card-version">v2.11.0.0</span>
      <span class="doc-card-arrow">Open →</span>
    </div>
  </a>

</div>

<style>
.doc-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.25rem;
  margin-top: 2rem;
}
.doc-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  text-decoration: none !important;
  color: inherit;
  background: #fff;
  transition: border-color 0.15s, box-shadow 0.15s, background 0.15s;
  cursor: pointer;
}
.doc-card:hover {
  border-color: #2c84fa;
  box-shadow: 0 4px 16px rgba(44,132,250,0.15);
  background: #f6f9ff;
  text-decoration: none !important;
}
.doc-card:hover .doc-card-arrow {
  color: #2c84fa;
}
.doc-card-body {
  flex: 1;
}
.doc-card h2 {
  margin: 0 0 0.5rem;
  font-size: 1.05rem;
  color: #1a1a2e;
  border: none;
}
.doc-card:hover h2 {
  color: #2c84fa;
}
.doc-card p {
  margin: 0 0 1rem;
  font-size: 0.875rem;
  color: #57606a;
  line-height: 1.55;
}
.doc-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid #e5e7eb;
}
.doc-card-version {
  font-size: 0.75rem;
  color: #57606a;
  background: #f0f4ff;
  padding: 0.2em 0.55em;
  border-radius: 4px;
  font-weight: 500;
}
.doc-card-arrow {
  font-size: 0.8rem;
  color: #8c9cb0;
  font-weight: 600;
  letter-spacing: 0.02em;
  transition: color 0.15s;
}
.doc-card-coming-soon {
  opacity: 0.55;
  cursor: default;
  pointer-events: none;
}
.doc-card-badge {
  font-size: 0.75rem;
  color: #fff;
  background: #8c9cb0;
  padding: 0.2em 0.55em;
  border-radius: 4px;
  font-weight: 500;
}
</style>
