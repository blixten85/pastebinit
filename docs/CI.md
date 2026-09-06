# CI och release

`.github/workflows/ci.yml` producerar `python` och kör projektets compile/test-verifiering.

`.github/workflows/release-deb.yml` är ett separat manuellt releaseflöde för en redan existerande release-tag och är inte en del av PR-CI.
