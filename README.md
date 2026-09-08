<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/lpogosu/lpogosu/main/assets/banner-dark.jpg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/lpogosu/lpogosu/main/assets/banner-light.jpg">
  <img alt="От железа до модели — инфраструктура и LLM-системы" src="https://raw.githubusercontent.com/lpogosu/lpogosu/main/assets/banner-light.jpg">
</picture>

Собираю платформы и то, что поверх них работает с языковыми моделями. Интересует
стык: не «прикрутить LLM к сервису», а довести её до состояния, в котором она
эксплуатируется как обычная нагрузка — с метриками, лимитами, стоимостью запроса
и понятным поведением при отказе.

<!-- repos:start -->

### Платформа

| Репозиторий | О чём |
|---|---|
| [ansible-infra](https://github.com/lpogosu/ansible-infra) | Ansible-роли под Debian и RHEL: CIS-хардненинг, docker host, nginx, haproxy, node_exporter, бэкапы. Molecule-тесты |
| [devsecops-pipeline](https://github.com/lpogosu/devsecops-pipeline) | Supply chain security: сканирование образов, SBOM, подпись Cosign, admission-политики. Демо, где сборка падает на CVE |
| [k8s-platform-gitops](https://github.com/lpogosu/k8s-platform-gitops) | GitOps-платформа на kind: ArgoCD app-of-apps, Helm + Kustomize overlays, ingress, cert-manager, sealed-secrets |
| [observability-stack](https://github.com/lpogosu/observability-stack) | Prometheus, Loki, Tempo, Grafana и Alertmanager как код. SLO, multi-burn-rate алерты и unit-тесты правил |
| [terraform-aws-modules](https://github.com/lpogosu/terraform-aws-modules) | Terraform-модули для AWS: VPC, EKS, RDS, S3 + CloudFront, OIDC-роли для CI |
| [terraform-yandex-modules](https://github.com/lpogosu/terraform-yandex-modules) | Библиотека Terraform-модулей для Yandex Cloud: VPC, Managed Kubernetes, PostgreSQL, Object Storage, ALB, IAM |

### CI/CD

| Репозиторий | О чём |
|---|---|
| [ci-templates](https://github.com/lpogosu/ci-templates) | Переиспользуемые workflow GitHub Actions и шаблоны GitLab CI: сборка, тесты, публикация образов, релизы по semver |
| [jenkins-shared-library](https://github.com/lpogosu/jenkins-shared-library) | Shared library для Jenkins: декларативные шаги сборки и деплоя, тесты пайплайнов на JenkinsPipelineUnit |
| [pipeline-doctor](https://github.com/lpogosu/pipeline-doctor) | Разбор упавших пайплайнов: извлечение причины из мегабайтного лога, кластеризация, доказанная флакость и стоимость в машинном времени |

### LLM и данные

| Репозиторий | О чём |
|---|---|
| [k8s-model-operator](https://github.com/lpogosu/k8s-model-operator) | Оператор Kubernetes для выката LLM: CRD, контроллер на controller-runtime, прогрев кэша весов и автоскейл по глубине очереди |
| [llm-gateway](https://github.com/lpogosu/llm-gateway) | Шлюз перед LLM-провайдерами: роутинг, semantic cache, rate limiting, учёт стоимости, Prometheus-метрики и трейсы |
| [rag-service](https://github.com/lpogosu/rag-service) | RAG без фреймворков: стратегии чанкинга, pgvector, BM25, RRF, реранкинг и харнесс, который всё это измеряет |
| [service-classifier](https://github.com/lpogosu/service-classifier) | Гибридный пайплайн, где LLM — только один этап из четырёх. GBM обошёл семь протестированных моделей |

### Эксплуатация

| Репозиторий | О чём |
|---|---|
| [dev-env](https://github.com/lpogosu/dev-env) | Воспроизводимое окружение разработчика: dotfiles, Neovim, tmux, zsh и bootstrap одной командой на Debian, Fedora и macOS |
| [k8s-troubleshoot-agent](https://github.com/lpogosu/k8s-troubleshoot-agent) | Диагностика проблем в кластере Kubernetes: сбор состояния, правила разбора типовых отказов и объяснение причины простым языком |
| [postgres-toolkit](https://github.com/lpogosu/postgres-toolkit) | Инструменты эксплуатации PostgreSQL: диагностика раздувания, анализ планов, проверка индексов, бэкап и восстановление на момент времени |

### Продукты и проектирование

| Репозиторий | О чём |
|---|---|
| [genesis-provider](https://github.com/lpogosu/genesis-provider) | Генератор интеграций с платёжными провайдерами: OpenAPI на входе, готовый Ruby-клиент, вебхуки и отчёт о покрытии на выходе |
| [insurance-sim](https://github.com/lpogosu/insurance-sim) | Симулятор управления личными рисками: полгода, шесть полисов и бюджет, которого на всё не хватает. Next.js, чистый движок с воспроизводимым seed, Telegram Mini App и бот |

<!-- repos:end -->

### Инструменты

`Kubernetes` · `Helm` · `ArgoCD` · `Terraform` · `Ansible` · `Docker` · `Jenkins` · `GitLab CI`
`Prometheus` · `Grafana` · `Loki` · `Istio` · `Linux` · `Nginx` · `HAProxy`
`Python` · `FastAPI` · `TypeScript` · `React` · `Go` · `PostgreSQL` · `Neo4j` · `Kafka` · `Redis`

### Хакатоны

- **IT Purple Hack 2026** — 1 место по сумме баллов трёх кейсов
- **MTS True Tech Hack 2026** — 2 место
- **АгроДжем 2025** — 1 место
