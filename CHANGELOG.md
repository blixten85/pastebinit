# Changelog

Structured changelog entries are maintained automatically by Release Please from the existing `v2.3.7` baseline onward. Releases `v2.1.3` through `v2.3.7` remain available in the GitHub Releases history.

## [2.4.4](https://github.com/Avkroken/Pastebinit/compare/v2.4.3...v2.4.4) (2026-09-06)


### Documentation

* förenkla REPO.md på svenska ([#224](https://github.com/Avkroken/Pastebinit/issues/224)) ([03fe73b](https://github.com/Avkroken/Pastebinit/commit/03fe73bd18e247e9250b4e4fb56049a376a5b051))

## [2.4.3](https://github.com/Avkroken/Pastebinit/compare/v2.4.2...v2.4.3) (2026-09-06)


### Fixes

* align issue classification caller contract ([#219](https://github.com/Avkroken/Pastebinit/issues/219)) ([811a476](https://github.com/Avkroken/Pastebinit/commit/811a4760d31dcb7cadc088f74672ca7de853b6cd))

## [2.4.2](https://github.com/Avkroken/Pastebinit/compare/v2.4.1...v2.4.2) (2026-09-05)


### Documentation

* clarify repository-specific governance ([#215](https://github.com/Avkroken/Pastebinit/issues/215)) ([e7e8461](https://github.com/Avkroken/Pastebinit/commit/e7e846176c312cbea455904fc1cee940489c4450))

## [2.4.1](https://github.com/Avkroken/Pastebinit/compare/v2.4.0...v2.4.1) (2026-09-05)


### Documentation

* rename governance file to REPO.md ([#213](https://github.com/Avkroken/Pastebinit/issues/213)) ([a8c4818](https://github.com/Avkroken/Pastebinit/commit/a8c481896a577c846c4624057f84887d16e662e0))

## [2.4.0](https://github.com/Avkroken/Pastebinit/compare/v2.3.7...v2.4.0) (2026-09-05)


### Features

* adopt Release PR workflow ([#197](https://github.com/Avkroken/Pastebinit/issues/197)) ([4aec051](https://github.com/Avkroken/Pastebinit/commit/4aec0513c417df47573488c0b7ae99dc8cec9bc6))
* enable metadata-only AI issue triage ([#185](https://github.com/Avkroken/Pastebinit/issues/185)) ([cae272c](https://github.com/Avkroken/Pastebinit/commit/cae272c2068b57ba23ddf7ebf689720a543b7d10))


### Fixes

* avoid invalid reusable-workflow variable context ([#200](https://github.com/Avkroken/Pastebinit/issues/200)) ([2935254](https://github.com/Avkroken/Pastebinit/commit/29352546e46b42fe78af253d402a560d6642204f))
* complete PR metadata reconciliation ([#198](https://github.com/Avkroken/Pastebinit/issues/198)) ([e67d61c](https://github.com/Avkroken/Pastebinit/commit/e67d61ce84dddcfd724b5a0ae109f86b70fe4f22))
* continue PR reconciliation after assignment errors ([e67d61c](https://github.com/Avkroken/Pastebinit/commit/e67d61ce84dddcfd724b5a0ae109f86b70fe4f22))
* härda watchdogens branch-age ([#173](https://github.com/Avkroken/Pastebinit/issues/173)) ([6403999](https://github.com/Avkroken/Pastebinit/commit/6403999a86e8378cf68b32df2dae4c40650e4fb5))
* isolate Codex remediation from watchdog ([#178](https://github.com/Avkroken/Pastebinit/issues/178)) ([ea0b3b4](https://github.com/Avkroken/Pastebinit/commit/ea0b3b49485b1228b2c5019fff83076b8060682b))
* let metadata reconciliation finish ([#204](https://github.com/Avkroken/Pastebinit/issues/204)) ([1234bc8](https://github.com/Avkroken/Pastebinit/commit/1234bc85e131bb6a008a09c91459cd0b77f4b6d5))
* preserve queued metadata events ([#203](https://github.com/Avkroken/Pastebinit/issues/203)) ([601d915](https://github.com/Avkroken/Pastebinit/commit/601d915d0e678bcafe16d3e1b7354b331bca2121))
* propagate metadata reconciliation failures ([#196](https://github.com/Avkroken/Pastebinit/issues/196)) ([2340eeb](https://github.com/Avkroken/Pastebinit/commit/2340eeb8c747d8890a995ddd587646cbe4a67bd1))
* propagate PR reconciliation listing failures ([2340eeb](https://github.com/Avkroken/Pastebinit/commit/2340eeb8c747d8890a995ddd587646cbe4a67bd1))
* reconcile Dependabot outside PR events ([#191](https://github.com/Avkroken/Pastebinit/issues/191)) ([243b42c](https://github.com/Avkroken/Pastebinit/commit/243b42cdb348b775a9918f589758c2adc3133b66))
* reconcile PR metadata on schedule ([7aa95d1](https://github.com/Avkroken/Pastebinit/commit/7aa95d1f7e720485e031996664af8038475458a7))
* reconcile PR metadata without target events ([#193](https://github.com/Avkroken/Pastebinit/issues/193)) ([8efad58](https://github.com/Avkroken/Pastebinit/commit/8efad58c67b559ea1755c858e1b13438d9843834))
* resolve release Gamnacken client ID centrally ([#201](https://github.com/Avkroken/Pastebinit/issues/201)) ([85f7aef](https://github.com/Avkroken/Pastebinit/commit/85f7aefa60a139f10a96ee5bb1d8cc151a6867dd))
* schedule PR metadata reconciliation ([#194](https://github.com/Avkroken/Pastebinit/issues/194)) ([7aa95d1](https://github.com/Avkroken/Pastebinit/commit/7aa95d1f7e720485e031996664af8038475458a7))
* serialize issue metadata routing ([#202](https://github.com/Avkroken/Pastebinit/issues/202)) ([3bd3da3](https://github.com/Avkroken/Pastebinit/commit/3bd3da388dc7e86eb50c7bd293bea3391b5d944a))
* serialize PR metadata reconciliation ([#199](https://github.com/Avkroken/Pastebinit/issues/199)) ([a0cc13b](https://github.com/Avkroken/Pastebinit/commit/a0cc13b7a027735b05547af729f07f2f0e1d35f4))
* use centrally resolved release client ID ([85f7aef](https://github.com/Avkroken/Pastebinit/commit/85f7aefa60a139f10a96ee5bb1d8cc151a6867dd))


### Refactoring

* use central metadata orchestrator ([#205](https://github.com/Avkroken/Pastebinit/issues/205)) ([69f14b2](https://github.com/Avkroken/Pastebinit/commit/69f14b2cf1f1cc6c8524f6a1ad4e63db24f9077c))


### Documentation

* align AGENTS merge policy ([#157](https://github.com/Avkroken/Pastebinit/issues/157)) ([53a6e5c](https://github.com/Avkroken/Pastebinit/commit/53a6e5c4482b607ca5b96669d68447d7b7b5d837))
* align AGENTS merge policy with repository settings ([53a6e5c](https://github.com/Avkroken/Pastebinit/commit/53a6e5c4482b607ca5b96669d68447d7b7b5d837))
* align CI merge policy ([#158](https://github.com/Avkroken/Pastebinit/issues/158)) ([f5ad587](https://github.com/Avkroken/Pastebinit/commit/f5ad587dd99ff0ab54eb9759737908c26a280767))
* align governance and CI documentation ([#189](https://github.com/Avkroken/Pastebinit/issues/189)) ([3d06c6c](https://github.com/Avkroken/Pastebinit/commit/3d06c6c53397fc0971e63e4e7e6fcd90ebbe4462))
* centralize agent policy ([#188](https://github.com/Avkroken/Pastebinit/issues/188)) ([b3f3416](https://github.com/Avkroken/Pastebinit/commit/b3f3416aa0d0ce6ccb9274bc7d6813b4de8430fb))
* consolidate authoritative AI agent policy ([#176](https://github.com/Avkroken/Pastebinit/issues/176)) ([3778ed1](https://github.com/Avkroken/Pastebinit/commit/3778ed16ec99f22d357f230c25fbf7ecd95601aa))
* frys PR-scope efter öppning ([75f6a60](https://github.com/Avkroken/Pastebinit/commit/75f6a607fda437ccfee41000145d87b8c2a9efde))
* inherit organization funding links ([#195](https://github.com/Avkroken/Pastebinit/issues/195)) ([249b2cb](https://github.com/Avkroken/Pastebinit/commit/249b2cbe4a1ae40e73d6cf99e3d6efda22f49957))
* rätta agent-reglerna som motsade praktiken ([2c66b49](https://github.com/Avkroken/Pastebinit/commit/2c66b49fe568caee670af475063170be74bf613a))
* rätta agent-reglerna som motsade praktiken ([#142](https://github.com/Avkroken/Pastebinit/issues/142)) ([cc19397](https://github.com/Avkroken/Pastebinit/commit/cc1939784d725a65cb3a27a3318543138f01fb67))
* skärp PR-gates och auto-merge ([#170](https://github.com/Avkroken/Pastebinit/issues/170)) ([07f794f](https://github.com/Avkroken/Pastebinit/commit/07f794fa4329d9951831659ba66855892ec39def))
* skriv in svarsformatet från i-have-adhd i AGENTS.md ([11538ce](https://github.com/Avkroken/Pastebinit/commit/11538ce0d4cad9b937269b1408eda06f4f148e78))
* skriv in svarsformatet från i-have-adhd i AGENTS.md ([#141](https://github.com/Avkroken/Pastebinit/issues/141)) ([570b69f](https://github.com/Avkroken/Pastebinit/commit/570b69fec35ecda01930f98106eeb391075e1453))
* standardize bug issue form ([11e03e9](https://github.com/Avkroken/Pastebinit/commit/11e03e9b29b80caa8f547792a4b08c18c37a2600))
* unify community health files ([#190](https://github.com/Avkroken/Pastebinit/issues/190)) ([11e03e9](https://github.com/Avkroken/Pastebinit/commit/11e03e9b29b80caa8f547792a4b08c18c37a2600))

## [2.1.2](https://github.com/blixten85/pastebinit/compare/v2.1.1...v2.1.2) (2026-05-01)


### Bug Fixes

* build.yml added build-essential ([3d3d70b](https://github.com/blixten85/pastebinit/commit/3d3d70b5880f17805da05521d6dd9933d2ecc336))
* replace GHCR_TOKEN with GITHUB_TOKEN for auto-merge ([8e76b9a](https://github.com/blixten85/pastebinit/commit/8e76b9ad88dcf1aa3ab75ee55c6eca6c6e7791ed))
* use github.token for dependabot auto-merge ([3d8bd79](https://github.com/blixten85/pastebinit/commit/3d8bd7975ad3715e1f48beaf5a0cb23cafe57730))

## [2.1.1](https://github.com/blixten85/pastebinit/compare/v2.1.0...v2.1.1) (2026-05-01)


### Bug Fixes

* missing GH_TOKEN env var in auto-merge.yml ([26990ac](https://github.com/blixten85/pastebinit/commit/26990ac8ca77fb1feaeb4ebe53af6c2f6b16afd9))

## [2.1.0](https://github.com/blixten85/pastebinit/compare/v2.0.0...v2.1.0) (2026-04-30)


### Features

* pastebinit v2.0.0 — complete rewrite from scratch ([#1](https://github.com/blixten85/pastebinit/issues/1)) ([2fd5baa](https://github.com/blixten85/pastebinit/commit/2fd5baa68b85c27b8709e578798c5eeaee208145))
