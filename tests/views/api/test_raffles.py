from flask import url_for
from datetime import timezone

from tests.factories import RaffleFactory


class TestNewRaffle:
    def test_no_params(self, authed_client):
        assert authed_client.post(url_for("api.new_raffle")).status_code == 422

    def test_params_failed_validation(self, authed_client):
        res = authed_client.post(url_for("api.new_raffle"), data=_invalid_form_params())
        assert res.status_code == 422

    def test_valid_params(self, authed_client, mocker):
        mocker.patch(
            "app.util.raffle_form_validator.RaffleFormValidator.run", lambda x: True
        )
        mocker.patch(
            "app.services.reddit_service.get_submission_by_url"
        ).return_value = {"id": "1a2b3c"}
        mocker.patch("app.jobs.raffle_job.raffle.queue")
        res = authed_client.post(url_for("api.new_raffle"), data=_valid_form_params())
        assert res.status_code == 202


def _valid_form_params():
    return {
        "submissionUrl": "https://redd.it/57xvjb",
        "winnerCount": 1,
        "minAge": 0,
        "minComment": 0,
        "minLink": 0,
        "ignoredUsers": "[]",
    }


def _invalid_form_params():
    return _valid_form_params().update({"winnerCount": 0})


def _stub_raffle_job(raffle_params, user, job_id):
    return [raffle_params, user, job_id]


class TestGetRaffleMetrics:
    def test_returns_expected_results(self, client, mocker):
        TEST_VANITY_METRICS = {
            "num_total_verified_raffles": 1,
            "num_total_winners": 1,
            "top_recent_subreddits": ["/r/ok"],
        }
        mocker.patch(
            "app.db.models.raffle.Raffle.get_vanity_metrics",
            lambda: TEST_VANITY_METRICS,
        )

        res = client.get(url_for("api.get_raffle_metrics"))

        assert res.status_code == 200
        assert res.get_json() == TEST_VANITY_METRICS


class TestGetRecentRaffles:
    def test_returns_expected_results(self, client, mocker):
        raffle = RaffleFactory.create(uses_combined_karma=True)

        res = client.get(url_for("api.get_recent_raffles"))

        assert res.status_code == 200
        assert res.get_json() == [
            {
                "created_at": raffle.created_at.replace(
                    tzinfo=timezone.utc
                ).timestamp(),
                "submission_title": raffle.submission_title,
                "submission_id": raffle.submission_id,
                "subreddit": raffle.subreddit,
                "url_path": url_for("raffles.show", submission_id=raffle.submission_id),
            }
        ]
